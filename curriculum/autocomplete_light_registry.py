from autocomplete_light import shortcuts as autocomplete_light

from .areas import TITOLO_STUDIO_CHOICES, PATENTE_CIVILE_CHOICES
from .models import Titolo


class TitoloAutocompletamento(autocomplete_light.AutocompleteModelBase):
    split_words = True
    search_fields = ['nome',]
    model = Titolo
    attrs = {
        'data-autocomplete-minimum-characters': 0,
        # 'placeholder':  # Placeholder is overridden in forms.py
    }

    def choices_for_request(self):
        r = self.request
        titoli_tipo = r.session.get('titoli_tipo')
        has_meta_referer = 'curriculum' in r.META.get('HTTP_REFERER', '')
        if titoli_tipo and has_meta_referer:
            self.choices = self.choices.filter(tipo=titoli_tipo)

        # Select only <inseribile_in_autonomia> records
        self.choices = self.choices.filter(inseribile_in_autonomia=True)
        
        # Filter by <area>
        area_id = r.GET.get('area', None)
        if area_id not in ['', None]:

            # Titoli CRI (TC)
            if titoli_tipo == Titolo.TITOLO_CRI:
                self.choices = self.choices.filter(goal__unit_reference=area_id)
            
            # Titoli di studio (TS)
            elif titoli_tipo == Titolo.TITOLO_STUDIO:
                self.choices = self.choices.filter(
                    nome__istartswith=TITOLO_STUDIO_CHOICES[int(area_id)][1])
                
            # Patenti civili (PP)
            elif titoli_tipo == Titolo.PATENTE_CIVILE:
                self.choices = self.choices.filter(
                    nome__istartswith=PATENTE_CIVILE_CHOICES[int(area_id)][1])
    
        return super().choices_for_request()


class TitoloCRIAutocompletamento(autocomplete_light.AutocompleteModelBase):
    model = Titolo
    split_words = True
    search_fields = ['nome', 'sigla',]
    attrs = {
        'data-autocomplete-minimum-characters': 1,
    }

    def choices_for_request(self):
        self.choices = self.choices.filter(
            tipo=Titolo.TITOLO_CRI,
            is_active=True,
            inseribile_in_autonomia=False,
            area__isnull=False,
            nome__isnull=False,
            cdf_livello__isnull=False,
        ).order_by('nome').distinct('nome')

        return super().choices_for_request()


autocomplete_light.register(TitoloAutocompletamento)
autocomplete_light.register(TitoloCRIAutocompletamento)
