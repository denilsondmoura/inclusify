import os
from datetime import datetime
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from axe_selenium_python import Axe
from django.urls import reverse
from apps.core.models import Postagem

class AccessibilityTestBase(StaticLiveServerTestCase):
    """
    Base para testes de acessibilidade usando axe-core.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        cls.driver = webdriver.Chrome(options=chrome_options)
        cls.driver.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def run_accessibility_test(self, path, context=None, rules=None, tags=None, page_name=None):
        """
        Executa o teste axe-core em uma rota.
        $: python manage.py test tests.accessibility

        :param path: URL path (ex: '/login/') ou full URL
        :param context: CSS selector para limitar análise (opcional)
        :param rules: dicionário axe rules para habilitar/desabilitar (opcional)
        :param tags: lista de tags axe para filtrar checagens (opcional)
        """
        # Constrói URL completo
        url = path if path.startswith('http') else f'{self.live_server_url}{path}'
        self.driver.get(url)

        axe = Axe(self.driver)
        axe.inject()

        # Monta options sem valores None para evitar o erro 'None is not defined'
        opts = {}
        if rules:
            opts['rules'] = rules
        if tags:
            opts['runOnly'] = {'type': 'tag', 'values': tags}

        # Executa o teste
        if context and opts:
            results = axe.run(context=context, options=opts)
        elif context:
            results = axe.run(context=context)
        elif opts:
            results = axe.run(options=opts)
        else:
            results = axe.run()

        # Imprime relatório e falha se houver violações
        violations = results.get('violations', [])
        if violations:
            os.makedirs('tests/reports', exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f'tests/reports/{page_name}_{timestamp}_report.json'
            axe.write_results(violations, filename)
            
        self.assertEqual(len(violations), 0, self._format_violations(violations))

    def _format_violations(self, violations):
        msg = ['\nErros de acessibilidade encontrados:']
        for v in violations:
            msg.append(f"\nRegra: {v['id']} - {v['description']}")
            for node in v['nodes']:
                msg.append(
                    f"  Elemento: {node['html']}\n  Mensagem: {node['failureSummary']}"
                )
        return '\n'.join(msg)


class TestAllPagesAccessibility(AccessibilityTestBase):
    def test_home_page(self):
        self.run_accessibility_test(path='/', page_name='home')
        
    def test_postagens_recentes_page(self):
        self.run_accessibility_test(path='/postagens/recentes/', page_name='postagens_recentes_list')

    def test_register_page(self):
        self.run_accessibility_test(path='/accounts/register/', page_name='register')

    def test_login_page(self):
        self.run_accessibility_test(path='/accounts/login/', page_name='login')
        
    def test_profile_page(self):
        self.run_accessibility_test(path='/accounts/profile/', page_name='profile')
        
    def test_password_reset_page(self):
        self.run_accessibility_test(path='/accounts/password_reset/', page_name='password_reset')
        self.run_accessibility_test(path='/accounts/password_reset/done', page_name='password_reset_done')
        self.run_accessibility_test(path='/accounts/reset/MQ/cq9hna-b6b5da129447cd9590c5b5c12d1c34d2/', page_name='password_reset_confirm')
        self.run_accessibility_test(path='/accounts/reset/done/', page_name='password_reset_complete')
    
    def test_postagem_create_page(self):
        self.run_accessibility_test(path='/postagens/nova/', page_name='postagem_create')
    
    def test_topicos_page(self):
        self.run_accessibility_test(path='/topicos/', page_name='topicos_list')
        # self.run_accessibility_test(path='/topicos/2/postagens/', page_name='topico_postagens_list')
        
    def test_postagem_detail_page(self):
        postagem = Postagem.objects.create(
            titulo='Teste de Acessibilidade',
            corpo='Conteúdo qualquer para popular o detalhe.'
        )
        url = reverse('postagem_detail', kwargs={'pk': postagem.id})
        self.run_accessibility_test(path=url, page_name='postagem_detail')
    