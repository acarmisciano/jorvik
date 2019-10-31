from datetime import datetime, timedelta
from django import forms
from django.forms import ModelForm

from .models import Survey, Question # SurveyResult


class QuestionarioForm(forms.Form):
    QGROUP_UTILITA_PERCEPITA = 1
    QGROUP_DOCENTI = 2
    QGROUP_ORGANIZZAZIONE = 3
    QGROUP_SERVIZI = 4

    CHOICES_1_10 = [(i, i) for i in range(1, 11)]

    step = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        self.invalid_survey_forms = False

        for f in ['me', 'course', 'instance', 'step', 'survey_result']:
            setattr(self, f, kwargs.pop(f))
        super().__init__(*args, **kwargs)

    @property
    def response_direttori(self):
        return list(self.survey_result.response_json['direttori'].keys())

    def populate_questions_inputs(self, survey, question_group_id, **kwargs):
        for question in survey.get_questions().filter(question_group__id=question_group_id):
            if not question.is_active:
                # skip inactive questions
                continue

            qid = question.qid
            self.fields[qid] = forms.CharField(label=question.text)

            if question.question_type == Question.RADIO:
                self.fields[qid].widget = forms.RadioSelect(choices=self.CHOICES_1_10)
            elif question.question_type == Question.TEXT:
                pass

    def process_qid(self, cd):
        QID_PREFIX = 'qid_'
        return {
            k.replace(QID_PREFIX, ''): v for k,v in cd.items() if k.startswith(QID_PREFIX)
        }


class QuestionarioPaginaIniziale(QuestionarioForm):
    # def process(self, result, next_step):
    #     super().process(result, next_step)
    pass


class SelectDirettoreCorsoForm(QuestionarioForm):
    direttore = forms.CharField(label="")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        direttori_choices = [(i.pk, i.nome_completo) for i in self.course.direttori_corso()]
        self.fields['direttore'].widget = forms.RadioSelect(choices=direttori_choices)

        response_direttori = self.response_direttori
        if response_direttori and len(response_direttori) >= 1:
            self.fields['direttore'].initial = response_direttori[0]

        self.fields['step'].initial = self.step

    def validate_questionario(self, result, **kwargs):
        form = self
        if form.is_valid():
            cd = form.cleaned_data
            direttore = cd['direttore']

            # Nel caso di direttori multipli ogni direttore ha una sua key (persona.pk)
            if direttore not in result.response_json['direttori']:
                result.response_json['direttori'][direttore] = {}
                result.save()

            # (success): da salvare nella view
            return True

        # Non da salvare
        return False


class ValutazioneDirettoreCorsoForm(QuestionarioForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        survey, course = self.instance, self.course

        # Per indicare con request.POST con che form/step stiamo lavorando
        self.fields['step'].initial = self.step

        self.populate_questions_inputs(self.instance, QuestionarioForm.QGROUP_UTILITA_PERCEPITA)

    def validate_questionario(self, result, **kwargs):
        direttore = kwargs.pop('direttore_da_valutare')

        form = self
        if form.is_valid():
            cd = form.cleaned_data

            risposte_valutazione_direttore = {k.replace('qid_', ''): v for k,v in cd.items() if k.startswith('qid_')}
            result.response_json['direttori'][str(direttore.pk)] = risposte_valutazione_direttore
            result.save()

            return True

        return False


class ValutazioneUtilitaLezioniForm(QuestionarioForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Per indicare con request.POST con che form/step stiamo lavorando
        self.fields['step'].initial = self.step

        # Risposte precedentemente salvate
        response_lezioni = self.survey_result.response_json['lezioni']

        for lezione in self.course.get_lezioni_precaricate():
            lezione_pk = 'lezioni_pk_%s' % lezione.pk

            # Crea i campi con 10 radio-button (0-10)
            self.fields[lezione_pk] = forms.CharField(label=lezione.nome)
            self.fields[lezione_pk].widget = forms.RadioSelect(choices=self.CHOICES_1_10)

            # Valorizzare gli input se ci sono le risposte
            lezione_pk_str = str(lezione.pk)
            if lezione_pk_str in response_lezioni:
                self.fields[lezione_pk].initial = response_lezioni[lezione_pk_str]

    def validate_questionario(self, result, **kwargs):
        form = self
        if form.is_valid():
            cd = form.cleaned_data

            if 'lezioni' not in result.response_json:
                result.response_json['lezioni'] = dict()

            lezioni_valutate = {k.replace('lezioni_pk_', ''): v for k, v in cd.items() if k.startswith('lezioni_pk_')}
            result.response_json['lezioni'] = lezioni_valutate
            result.save()

            return True
        return False


class ValutazioneDocenteCorsoForm(QuestionarioForm):
    docente_lezione_pk = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Per indicare con request.POST con che form/step stiamo lavorando
        self.fields['step'].initial = self.step

        # Prima generare la struttura
        self.generate_json_structure()

        # Creare gli input per la valutazione di ogni docente per ogni singola lezione
        self.populate_questions_inputs(self.instance, QuestionarioForm.QGROUP_DOCENTI)

        # Per indicare con request.POST che docente/lezione valutiamo
        docente_lezione = self.survey_result.get_uncompleted_valutazione_docente_lezione()
        self.fields['docente_lezione_pk'].initial = "%s_%s" % docente_lezione

    def generate_json_structure(self):
        """
        Questo metodo genera la struttura delle chiavi delle lezioni (JSON).
        Formato:
        {
            'lezioni': {
                'docente.pk': {
                    'lezione.pk': {
                        "completed": true|false,
                        "domanda.pk": "risposta 1-10",
                        "domanda.pk": "risposta 1-10",
                        ...
                    },
                    ...
                },
                ...
            }
        }

        :return: None
        """

        lezioni_struttura = self.survey_result.response_json['lezioni']
        for lezione in self.course.lezioni.all():

            # Per docenti (Persona)
            for docente_pk in lezione.docente.all().values_list('pk', flat=True):
                docente_pk = str(docente_pk)
                lezione_pk = str(lezione.pk)

                # Crea dict vuoti
                if docente_pk not in lezioni_struttura:
                    lezioni_struttura[docente_pk] = dict()

                if lezione_pk not in lezioni_struttura[docente_pk]:
                    lezioni_struttura[docente_pk][lezione_pk] = dict(completed=False)

            # # Per docenti esterni
            # docente_esterno = lezione.docente_esterno
            # if docente_esterno:
            #     if docente_esterno not in lezioni_struttura:
            #         lezioni_struttura[docente_esterno] = dict()
            #     lezioni_struttura[docente_esterno][lezione.pk] = dict(completed=False)

        # Salva la struttura
        self.survey_result.save()

    def validate_questionario(self, result, **kwargs):
        form = self
        if form.is_valid():
            cd = form.cleaned_data

            docente, lezione = cd['docente_lezione_pk'].split('_')

            risposte = self.process_qid(cd)
            risposte['completed'] = True

            result.response_json['lezioni'][docente][lezione] = risposte
            result.save()

            return True
        return False


class RespondToCourseSurveyForm(ModelForm):
    class Meta:
        model = Survey
        fields = ['text']

    def __init__(self, *args, **kwargs):
        self.me = kwargs.pop('me')
        self.course = kwargs.pop('course')
        super().__init__(*args, **kwargs)
        self.fields.pop('text')

        # survey = self.instance
        # responses = survey.get_responses_dict(self.me)
        # for question in survey.get_questions():
        #     if not question.is_active:
        #         # skip inactive questions
        #         continue
        #
        #     qid = question.qid
        #     self.fields[qid] = forms.CharField(label=question.text)
        #     field = self.fields[qid]
        #
        #     if qid in responses:
        #         # Set input values if user has already voted
        #         response_for_question = responses[qid]
        #         field.initial = response_for_question['response']
        #
        #         # Disable editing after N time passed since user voted
        #         delta = datetime.now() - response_for_question['object'].created_at
        #         if delta >= timedelta(days=2):
        #             field.widget.attrs["disabled"] = "disabled"
        #
        #     if survey.is_course_admin(self.me, self.course):
        #         # Director of course can see questions but cannot vote
        #         field.widget.attrs["disabled"] = "disabled"
        #
        #     if question.required:
        #         field.required = True
        #         field.widget.attrs["class"] = "required"
        #     else:
        #         field.required = False
