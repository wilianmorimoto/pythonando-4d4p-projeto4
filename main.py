import flet as ft
import requests
from connect import get_livros
from urllib.parse import urlparse, parse_qs


def main(page: ft.Page):
  page.title = 'Cadastro App'
  page.window.width = 400

  def home_page():
    nome_input = ft.TextField(label='Nome do produto',
                              text_align=ft.TextAlign.LEFT)
    streaming_select = ft.Dropdown(
        label='Selecione o streaming',
        options=[
            ft.dropdown.Option('AK', text='Amazon Kindle'),
            ft.dropdown.Option('F', text='Físico'),
        ]
    )
    cat_sus_check = ft.Checkbox(label='Suspense')
    cat_ter_check = ft.Checkbox(label='Terror')
    cat_ave_check = ft.Checkbox(label='Aventura')
    cat_edu_check = ft.Checkbox(label='Educação')

    def carregar_livros():
      lista_livros.controls.clear()
      for i in get_livros():
        lista_livros.controls.append(
            ft.Container(
                ft.Text(i['nome']),
                bgcolor=ft.colors.BLACK12,
                padding=15,
                alignment=ft.alignment.center,
                border_radius=10,
                margin=3,
                on_click=lambda e, livro_id=i['id']: page.go(f'/review?id={livro_id}')
            )
        )
      page.update()

    def cadastrar(e):
      data = {
          'nome': nome_input.value,
          'streaming': streaming_select.value,
          'categorias': []
      }
      if cat_sus_check.value:
        data['categorias'].append(1),
      if cat_ter_check.value:
        data['categorias'].append(2),
      if cat_ave_check.value:
        data['categorias'].append(3),
      if cat_edu_check.value:
        data['categorias'].append(4),

      requests.post('http://127.0.0.1:8000/api/livros/', json=data)
      carregar_livros()

    cadastrar_btn = ft.ElevatedButton('Cadastrar', on_click=cadastrar)

    lista_livros = ft.ListView()

    carregar_livros()

    page.views.append(
        ft.View(
            '/',
            controls=[
                nome_input,
                streaming_select,
                cat_sus_check,
                cat_ter_check,
                cat_ave_check,
                cat_edu_check,
                cadastrar_btn,
                lista_livros,
            ]
        )
    )

  def review_page(livro_id):
    def avaliar(e):
      data = {
          'nota': int(nota_input.value),
          'comentarios': comentario_input.value
      }

      try:
        res = requests.put(f'http://127.0.0.1:8000/api/livros/{livro_id}', json=data)
        if res.status_code == 200:
          page.snack_bar = ft.SnackBar(ft.Text('Avaliação enviada!'))
        else:
          page.snack_bar = ft.SnackBar(ft.Text('Erro ao enviar avaliação.'))
        page.snack_bar.open = True
      except:
        page.snack_bar = ft.SnackBar(ft.Text(f'Erro de conexão: {Exception}'))
        page.snack_bar.open = True
      page.update()
      page.go('/')

    nota_input = ft.TextField(label='Nota (inteiro)', value=0, width=120, text_align=ft.TextAlign.LEFT)
    comentario_input = ft.TextField(label='Comentário', multiline=True, expand=True)
    avaliar_btn = ft.ElevatedButton('Avaliar', on_click=avaliar)
    voltar_btn = ft.ElevatedButton('Voltar', on_click=lambda e: page.go('/'))

    page.views.append(
        ft.View(
            '/review',
            controls=[
                nota_input,
                comentario_input,
                avaliar_btn,
                voltar_btn,
            ]
        )
    )

  def route_change(e):
    page.views.clear()

    if page.route == '/':
      home_page()
    elif page.route.startswith('/review'):
      parsed_url = urlparse(page.route)
      query_params = parse_qs(parsed_url.query)
      livro_id = query_params['id'][0]
      review_page(livro_id)
    page.update()

  page.on_route_change = route_change
  page.go('/')


ft.app(target=main)
