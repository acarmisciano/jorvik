from django_cron import CronJobBase, Schedule

from formazione.models import CorsoBase


class CronNotificaCorsiBaseDaAttivare(CronJobBase):

    RUN_EVERY_HOURS = 24
    RUN_EVERY_MINS = RUN_EVERY_HOURS * 60
    RUN_AT_TIMES = ['6:30']

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'base.corsibase.notifica'

    def do(self):
        pendenti = CorsoBase.attivazione_pendente()
        for p in pendenti:
            p.informa_presidente()
