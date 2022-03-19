from django.views.generic.base import TemplateView


class AboutAuthorView(TemplateView):
    template_name = 'about/author.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['just_title'] = 'Страница об авторе'
        context['just_text'] = ('Нау́ка — деятельность, направленная на'
                                'выработку и систематизацию объективных'
                                'знаний о действительности.'
                                )
        return context


class AboutTechView(TemplateView):
    template_name = 'about/tech.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['just_title'] = 'Страница о науке и технологиях '
        context['just_text'] = ('Эта деятельность осуществляется путём сбора'
                                'фактов, их регулярного обновления,'
                                'систематизации и критического анализа.'
                                'На этой основе выполняется обобщения или'
                                'синтез новых знаний, которые описывают'
                                'наблюдаемые природные или общественные'
                                'явления и указывают на причинно-следственные'
                                'связи, что позволяет осуществить '
                                'прогнозирование. Те гипотезы, которые'
                                'описывают совокупность наблюдаемых фактов и'
                                'не опровергаются экспериментами, признаются'
                                'законами природы или общества'
                                )
        return context
