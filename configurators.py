
class LaLigaConfig(object):

    def __init__(self):

        self.competition = 'LaLiga'

        self.str_links='Consulta el directo</strong>'
        self.str_time = 'Consulta el directo</strong>'

        self.str_extract_links_pre = '<a class="cont-txt-info-evento" href="'
        self.str_extract_links_after = '/narracion/">\n<span class="'

        self.str_extract_times_pre = '<time itemprop="startDate" content="'
        self.str_extract_times_after = '"></time>'

    def number_games(self, rnd):
        return 10
