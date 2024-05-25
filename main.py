from typing import Annotated

from fastapi import FastAPI, HTTPException, APIRouter
from fastapi.responses import HTMLResponse
from fastui import FastUI, AnyComponent, prebuilt_html, components as c
from fastui.components.display import DisplayMode, DisplayLookup
from fastui.events import GoToEvent, BackEvent
from fastui.forms import fastui_form
from pydantic import BaseModel, Field
import data

app = FastAPI()


# uvicorn olimp_7:app --reload #Запуск приложения
# data.post_debug(from_string, what_string)
# -------------------classes----------------------
class Ebz(BaseModel):
    son: str = Field(title='son')
    father: str = Field(title='father')


class Ebz_chain(BaseModel):
    chain: str = Field(title='chain')


class Proj(BaseModel):
    project: str = Field(title='project')
    skills: str = Field(title='skills')


class LoginForm(BaseModel):
    proj: str = Field(
        title='Email Address',
        description='Enter whatever value you like', json_schema_extra={'autocomplete': 'email'}
    )


class Candidate(BaseModel):
    cand_skills: str = Field(title='skills')


class SkillChain(BaseModel):
    skill: str = Field(title='skill')
    chain: str = Field(title='chain')


class SkillProj(BaseModel):
    skill: str = Field(title='skill')
    projects: str = Field(title='projects')


class ProjName(BaseModel):
    proj_name: str = Field(title='proj_name')


# -----------inittial data------------------------
dct = data.get_ebz()
dct_proj = data.get_proj()
txt_cand = data.get_candidate()
dct_projname = data.get_projname()

ebz_lst = []
for i in sorted(dct, key=lambda x: dct[x]):
    ebz_lst.append(Ebz(son=i, father=dct[i]))
chain_lst = []
for i in sorted(dct, key=lambda x: dct[x]):
    cur = [i]
    while i != '_root' and i != 'INCORRECT!!!':
        i = dct.get(i, 'INCORRECT!!!')
        cur.append(i)
    chain_lst.append(Ebz_chain(chain=' -> '.join(cur)))


# ---------------------main menu--------------------
@app.get('/api/', response_model=FastUI, response_model_exclude_none=True)
def main_menu() -> list[AnyComponent]:
    return [
        c.Page(  # Page provides a basic container for components
            components=[
                c.Div(
                    components=[
                        c.Heading(text='Cистема поиска проекта для кандидата', level=1),
                        c.Heading(text='Главное меню', level=3),
                        c.LinkList(
                            links=[
                                c.Link(
                                    components=[c.Text(text='1. Работа с ЕБЗ (единая база знаний)')],
                                    on_click=GoToEvent(url='/ebz/'),
                                ),
                                c.Link(
                                    components=[c.Text(text='2. Работа с информацией о проектах (профиль и т.д.)')],
                                    on_click=GoToEvent(url='/project/'),
                                ),
                                c.Link(
                                    components=[c.Text(text='3. Работа с профилем кандидата')],
                                    on_click=GoToEvent(url='/candidate/'),
                                ),
                                # c.Link(
                                #     components=[c.Text(text='4. Работа с профилем профессии')],
                                #     on_click=GoToEvent(url='/prof/'),
                                # ),
                            ],
                        ),
                        c.Markdown(

                            text="""\
    ________________________________________________________________________________________

    Система поиска проекта, подходящего для кандидата наилучшим образом, построена на основе: 

    *   единой базы знаний (ЕБЗ),
    *   описания знаний и умений для каждого проекта,
    *   знаний и умений каждого кандидата.

    ЕБЗ построена в виде набора пар "сын" -> "отец", которые соединяются в цепочку, например:
    python -> языки программирования -> программирование -> информационные технологии (от частного к общему)
    или 
    поиск кандидатов -> менеджмент

    Оценка соответствия кандидата и проекта производится посредством сравнения умений кандидата и требований проекта
    на основе единой базы знаний

    Вы работаете с версией v.0.7

    """
                        ),
                    ],
                    class_name='border-top mt-3 pt-1',
                ),
            ]
        ),
    ]


@app.get('/api/in_dev/', response_model=FastUI, response_model_exclude_none=True)
def menu_ebz() -> list[AnyComponent]:
    return [
        c.Page(
            components=[
                c.Div(
                    components=[
                        c.Heading(text='Этот режим еще в разработке!', level=2),
                    ],
                    class_name='border-top mt-3 pt-1',
                ),
                c.Div(
                    components=[
                        c.Heading(text='________________________________', level=3),
                        c.Link(components=[c.Text(text='Назад к предыдущему режиму')], on_click=BackEvent()),
                    ]
                )
            ]
        ),
    ]


# -------------------------ebz-----------------------------
@app.get('/api/ebz/', response_model=FastUI, response_model_exclude_none=True)
def menu_ebz() -> list[AnyComponent]:
    return [
        c.Page(
            components=[
                c.Div(
                    components=[
                        c.Heading(text='Единая база знаний (ЕБЗ)', level=1),
                        c.Heading(text='Меню подсистемы ЕБЗ', level=3),
                        # c.Markdown(
                        #     text=(
                        #         'Меню подсистемы "ЕБЗ"'
                        #         '                     '
                        #     )
                        # ),
                        c.LinkList(
                            links=[
                                c.Link(
                                    components=[c.Text(text='1. Просмотр (элемент -> элемент)')],
                                    on_click=GoToEvent(url='/ebz_lst/'),
                                ),
                                c.Link(
                                    components=[c.Text(text='2. Просмотр (цепочки элементов)')],
                                    on_click=GoToEvent(url='/ebz_chain/'),
                                ),
                                c.Link(
                                    components=[c.Text(text='3. Поиск по ключевому слову')],
                                    on_click=GoToEvent(url='/in_dev/'),
                                ),
                                # c.Link(
                                #     components=[c.Text(text='4. Добавление элемента знаний')],
                                #     on_click=GoToEvent(url='/in_dev/'),
                                # ),
                                c.Link(
                                    components=[c.Text(text='4. Проверка корректности ЕБЗ')],
                                    on_click=GoToEvent(url='/ebz_check/'),
                                ),
                                c.Link(
                                    components=[c.Text(text='6. Коррекция элемента знаний')],
                                    on_click=GoToEvent(url='/in_dev/'),
                                ),
                                c.Link(
                                    components=[c.Text(text='7. Удаление элемента знаний')],
                                    on_click=GoToEvent(url='/in_dev/'),
                                ),

                            ],
                        ),
                        c.Markdown(

                            text="""\
    ________________________________________________________________________________________

    Подсистема работы с единой базой знаний предназначена для унификации представления информации о проектах и
    информации об знаниях и умениях кандидатов.  

    ЕБЗ построена в виде набора пар "сын" -> "отец", которые соединяются в цепочку, например:
    python -> языки программирования -> программирование -> информационные технологии (от частного к общему)
    или 
    поиск кандидатов -> менеджмент

    Оценка соответствия кандидата и проекта производится посредством сравнения умений кандидата и требований проекта
    на основе единой базы знаний
    """
                        ),

                    ],
                    class_name='border-top mt-3 pt-1',
                ),
                c.Div(
                    components=[
                        c.Heading(text='________________________________', level=3),
                        c.Link(components=[c.Text(text='Назад к предыдущему режиму')], on_click=GoToEvent(url='/')),
                    ]
                )
            ]
        ),
    ]


@app.get('/api/ebz_lst/', response_model=FastUI, response_model_exclude_none=True)
def ebz_table() -> list[AnyComponent]:
    ebz_lst = []
    for i in sorted(dct, key=lambda x: dct[x]):
        ebz_lst.append(Ebz(son=i, father=dct[i]))
    return [
        c.Page(  # Page provides a basic container for components
            components=[
                c.Heading(text='Единая база знаний (элемент -> элемент)', level=1),
                c.Table(
                    data=ebz_lst,  # users
                    columns=[
                        DisplayLookup(field='son', table_width_percent=20),
                        DisplayLookup(field='father', table_width_percent=20),
                    ],

                ),

                # c.Button(text = "Добавить новый элемент", on_click=GoToEvent(url='/pair/add/')),
                c.Div(
                    components=[
                        c.Heading(text='________________________________', level=3),
                        c.Button(text="Добавить новый элемент", on_click=GoToEvent(url='/pair/add/')),
                        c.Button(text="Назад к предыдущему режиму", on_click=GoToEvent(url='/ebz/')),
                        # c.Link(components=[c.Text(text='Назад к предыдущему режиму')], on_click=GoToEvent(url='/ebz/')),

                    ]
                ),
            ]
        ),
    ]


@app.get('/api/ebz_check/', response_model=FastUI, response_model_exclude_none=True)
def ebz_table_check() -> list[AnyComponent]:
    chain_lst = []
    for i in sorted(dct):
        cur = [i]
        while i != '_root' and i != 'INCORRECT!!!':
            i = dct.get(i, 'INCORRECT!!!')
            cur.append(i)
            if i == '_root':
                cur.append('CORRECT')
        chain_lst.append(Ebz_chain(chain=' -> '.join(cur)))

    return [
        c.Page(  # Page provides a basic container for components
            components=[
                c.Heading(text='Проверка корректности ЕБЗ', level=1),
                c.Table(
                    data=chain_lst,
                    columns=[
                        DisplayLookup(field='chain', table_width_percent=50),
                    ],
                ),
                c.Div(
                    components=[
                        c.Heading(text='________________________________', level=3),
                        c.Link(components=[c.Text(text='Назад к предыдущему режиму')], on_click=BackEvent()),
                    ]
                ),
            ]
        ),
    ]


@app.get('/api/ebz_chain/', response_model=FastUI, response_model_exclude_none=True)
def ebz_table_chain() -> list[AnyComponent]:
    chain_lst = []
    for i in sorted(dct):  # , key=lambda x: dct[x]):
        cur = [i]
        while i != '_root' and i != 'INCORRECT!!!':
            i = dct.get(i, 'INCORRECT!!!')
            cur.append(i)
        # while i != '_root':
        #     i = dct[i]
        #     cur.append(i)
        chain_lst.append(Ebz_chain(chain=' -> '.join(cur)))

    return [
        c.Page(  # Page provides a basic container for components
            components=[
                c.Heading(text='Единая база знаний (цепочки элементов)', level=1),
                c.Table(
                    data=chain_lst,
                    columns=[
                        DisplayLookup(field='chain', table_width_percent=50),
                    ],
                ),
                c.Div(
                    components=[
                        c.Heading(text='________________________________', level=3),
                        c.Link(components=[c.Text(text='Назад к предыдущему режиму')], on_click=BackEvent()),
                    ]
                ),
            ]
        ),
    ]


@app.post('/api/pair/')  # , response_model=FastUI, response_model_exclude_none=True)
def add_pair(form: Annotated[Ebz, fastui_form(Ebz)]):
    new_ebz = Ebz(**form.model_dump())
    ebz_lst.append(new_ebz)
    dct[new_ebz.son] = new_ebz.father
    data.post_ebz(dct)
    return [c.FireEvent(event=GoToEvent(url='/ebz_lst/'))]


@app.get('/api/pair/add/', response_model=FastUI, response_model_exclude_none=True)
def add_pair_page():
    return [
        c.Page(
            components=[
                c.Heading(text='Элементы', level=1),
                c.ModelForm(
                    model=Ebz,
                    submit_url='/api/pair/'),
                c.Link(components=[c.Text(text='Назад к предыдущему режиму')], on_click=BackEvent()),
            ]
        )
    ]


# ---------------projects--------------------------------
@app.get('/api/project/', response_model=FastUI, response_model_exclude_none=True)
def menu_project() -> list[AnyComponent]:
    return [
        c.Page(
            components=[
                c.Div(
                    components=[
                        c.Heading(text='Информация о проекте', level=1),
                        c.Heading(text='Меню подсистемы "Проект"', level=3),

                        c.LinkList(
                            links=[
                                c.Link(
                                    components=[c.Text(text='1. Просмотр списка проектов')],
                                    on_click=GoToEvent(url='/projspis/'),
                                ),
                                c.Link(
                                    components=[c.Text(text='2. Выбор имени проекта')],
                                    on_click=GoToEvent(url='/proj_new/'),
                                ),
                                # c.Link(
                                #     components=[c.Text(text='3. Коррекция профиля проекта')],
                                #     on_click=GoToEvent(url='/in_dev/'),
                                # ),
                                c.Link(
                                    components=[c.Text(text='3. Проверка соответствия профиля проекта и ЕБЗ')],
                                    on_click=GoToEvent(url='/proj_chain/'),
                                ),

                                c.Link(
                                    components=[c.Text(text='4. Работа с информацией о проекте')],
                                    on_click=GoToEvent(url='/in_dev/'),
                                ),
                            ],
                        ),
                        c.Markdown(

                            text="""\
        ________________________________________________________________________________________

        Подсистема "Проект" предназначена для унифицированного описания технологий, знаний и умений, которые используются
        в каждом проекте.

        Возможно использование как технологий, которые есть в ЕБЗ, так и тех уникальных знаний, которые в ЕБЗ нет
        (в качестве исключений).  

        В этом случае сравнение со знаниями кандидата фиксируеся в случае полного совпадения.
        Если же технологии есть в ЕБЗ, то возможно более гибкое сравнение по длине цепочек, совпадающих у кандидата и проекта.
        """
                        ),
                    ],
                    class_name='border-top mt-3 pt-1',
                ),
                c.Div(
                    components=[
                        c.Heading(text='________________________________', level=3),
                        c.Link(components=[c.Text(text='Назад к предыдущему режиму')], on_click=GoToEvent(url='/')),
                    ]
                )
            ]
        ),
    ]


@app.get('/api/projspis/', response_model=FastUI, response_model_exclude_none=True)
def proj_table() -> list[AnyComponent]:
    proj_lst = []
    for i in dct_proj:  # sorted(dct_proj, key=lambda x: dct_proj[x]):
        proj_lst.append(Proj(project=i, skills=dct_proj[i]))
    return [
        c.Page(  # Page provides a basic container for components
            components=[
                c.Heading(text='Список проектов', level=1),
                c.Table(
                    data=proj_lst,  # users
                    columns=[
                        DisplayLookup(field='project', table_width_percent=20),
                        DisplayLookup(field='skills', table_width_percent=40),
                    ],

                ),

                c.Div(
                    components=[
                        c.Heading(text='________________________________', level=3),
                        c.Button(text="Добавить новый проект", on_click=GoToEvent(url='/proj/add/')),
                        c.Button(text="Назад к предыдущему режиму", on_click=GoToEvent(url='/project/')),
                    ]
                ),
            ]
        ),
    ]


@app.post('/api/new_proj/')
def add_pair(form: Annotated[ProjName, fastui_form(ProjName)]):
    new_pro = ProjName(**form.model_dump())
    dct_projname['proj_name'] = new_pro.proj_name
    data.post_projname(dct_projname)
    return [c.FireEvent(event=GoToEvent(url='/project/'))]


@app.get('/api/proj_new/', response_model=FastUI, response_model_exclude_none=True)
def select() -> list[AnyComponent]:
    return [
        c.Page(
            components=[
                c.Heading(text='Имя проекта', level=1),
                c.Heading(text=dct_projname['proj_name'], level=3),
                c.ModelForm(
                    model=ProjName,
                    submit_url='/api/new_proj/'),
                c.Link(components=[c.Text(text='Назад к предыдущему режиму')], on_click=BackEvent()),
            ]
        )
    ]


@app.get('/api/proj_chain/', response_model=FastUI, response_model_exclude_none=True)
def skill_ebz_chain() -> list[AnyComponent]:
    dct_proj = data.get_proj()
    dct_projname = data.get_projname()
    chain_lst = []

    for s in dct_proj[dct_projname['proj_name']].split():
        cur = []
        i = s
        while i in dct:
            cur.append(i)
            i = dct[i]
        if cur:
            chain_lst.append(SkillChain(skill=s, chain='->'.join(cur)))
        else:
            chain_lst.append(SkillChain(skill=s, chain='Not in EBZ'))
    return [
        c.Page(  # Page provides a basic container for components
            components=[
                c.Heading(text=dct_projname['proj_name'] + ' -> Единая база знаний', level=2),
                c.Table(
                    data=chain_lst,
                    columns=[
                        DisplayLookup(field='skill', table_width_percent=20),
                        DisplayLookup(field='chain', table_width_percent=50),
                    ],
                ),
                c.Div(
                    components=[
                        c.Heading(text='________________________________', level=3),
                        c.Link(components=[c.Text(text='Назад к предыдущему режиму')], on_click=BackEvent()),
                    ]
                ),
            ]
        ),
    ]


def skill_projects(s, p):
    result = 0
    if s not in dct:
        return 100 if set(s.split()) & set(dct_proj[p].split()) else 0
    else:
        chain_p = []
        chain_s = []
        while s in dct:
            chain_s.append(s)
            s = dct.get(s, 'stop')
        for i in dct_proj[p].split():
            if i in dct:
                chain_p = []
                while i in dct:
                    chain_p.append(i)
                    i = dct.get(i, 'stop')
            if set(chain_s) & set(chain_p):
                result = max(result, len(set(chain_s) & set(chain_p)) / (min(len(chain_s), len(chain_p))) * 100)
    return result


@app.get('/api/skill_proj/', response_model=FastUI, response_model_exclude_none=True)
def skill_proj() -> list[AnyComponent]:
    txt_cand = data.get_candidate()
    dct_proj = data.get_proj()
    n10 = 15
    probel = '_'
    _n10 = '.' * n10
    head = ''  # _n10.join(dct_proj)
    for i in dct_proj:
        head += i + probel * (n10 - len(i) + 1)
    head = head.strip(probel)
    chain_lst = [SkillProj(skill="    ", projects=head)]
    total = {}
    for s in txt_cand.split():
        if True:
            res = ''
            for i in dct_proj:
                result = skill_projects(s, i)
                total[i] = total.get(i, 0) + result
                x = str(int(result)) + '%'
                res += x + probel * (n10 - len(x))
            res = res.strip(probel)
            chain_lst.append(SkillProj(skill=s, projects=res))
    total_str = ''
    for i in dct_proj:
        x = str(int(total.get(i, 0))) + '%'
        total_str += x + probel * (n10 - len(x))
    total_str = total_str.strip(probel)
    chain_lst.append(SkillProj(skill="TOTAL", projects=total_str))

    return [
        c.Page(  # Page provides a basic container for components
            components=[
                c.Heading(text='Кандидат -> Проекты', level=1),
                c.Table(
                    data=chain_lst,
                    columns=[
                        DisplayLookup(field='skill', table_width_percent=20),
                        DisplayLookup(field='projects', table_width_percent=50),
                    ],
                ),
                c.Div(
                    components=[
                        # c.Heading(text='________________________________', level=3),
                        c.Markdown(

                            text="""\
    ________________________________________________________________________________________
    Слева навыки кандидата (skills).
    Справа проекты и оценка соответствия каждого навыка кандидата требованиям проекта (в процентах).
    Оценки суммируются. Чем больше сумма, тем больше проект подходит кандидату.
    """
                        ),
                        c.Link(components=[c.Text(text='Назад к предыдущему режиму')], on_click=BackEvent()),
                    ]
                ),
            ]
        ),
    ]


@app.get('/api/proj/add/', response_model=FastUI, response_model_exclude_none=True)
def add_proj_page():
    return [
        c.Page(
            components=[
                c.Heading(text='Проект', level=1),
                c.ModelForm(
                    model=Proj,
                    submit_url='/api/projpair/'),
                c.Link(components=[c.Text(text='Назад к предыдущему режиму')], on_click=BackEvent()),
            ]
        )
    ]


@app.post('/api/projpair/')  # , response_model=FastUI, response_model_exclude_none=True)
def add_proj(form: Annotated[Proj, fastui_form(Proj)]):
    new_proj = Proj(**form.model_dump())
    dct_proj[new_proj.project] = new_proj.skills
    data.post_proj(dct_proj)
    return [c.FireEvent(event=GoToEvent(url='/projspis/'))]


# ------------------profession---------------------
# --------------------------candidate-------------------------
@app.get('/api/candidate/', response_model=FastUI, response_model_exclude_none=True)
def menu_candidate() -> list[AnyComponent]:
    return [
        c.Page(
            components=[
                c.Div(
                    components=[
                        c.Heading(text='Работа с профилем кандидата', level=1),
                        c.Heading(text='Меню подсистемы "Кандидат"', level=3),

                        # c.Markdown(
                        #     text=(
                        #         '======================================='
                        #     )
                        # ),
                        c.LinkList(
                            links=[
                                c.Link(
                                    components=[c.Text(text='1. Ввод и коррекция профиля кандидата')],
                                    on_click=GoToEvent(url='/candi_skills/'),
                                ),
                                c.Link(
                                    components=[c.Text(text='2. Проверка соответствия профиля кандидата и ЕБЗ')],
                                    on_click=GoToEvent(url='/skill_chain/'),
                                ),
                                c.Link(
                                    components=[
                                        c.Text(text='3. Оценка соответствия профиля кандидата профилю проектов')],
                                    on_click=GoToEvent(url='/skill_proj/'),
                                ),
                                # c.Link(
                                #     components=[c.Text(text='3. Оценка соответствия профиля кандидата профилю профессий')],
                                #     on_click=GoToEvent(url='/in_dev/'),
                                # ),
                            ],
                        ),
                        c.Markdown(

                            text="""\
    ________________________________________________________________________________________

    Подсистема "Кандидат" предназначена для унифицированного описания знаний и умений кандидата.

    Возможна проверка соответствия элементов знаний ЕБЗ.  

    В режиме проверки соответствия кандидата и проектов оцениваются, насколько кандидат соответствует проекту.
    Оценка проводится для каждого элемента знания, полное совпадение оценивается как 100%, затем оценки суммируются.
    Кандидат может выбрать проект, который наибольше соответствует его знаниям.
    """
                        ),

                    ],
                    class_name='border-top mt-3 pt-1',
                ),
                c.Div(
                    components=[
                        c.Heading(text='________________________________', level=3),
                        c.Link(components=[c.Text(text='Назад к предыдущему режиму')], on_click=GoToEvent(url='/')),
                    ]
                )
            ]
        ),
    ]


@app.post('/api/candi/')  # , response_model=FastUI, response_model_exclude_none=True)
def add_skills(form: Annotated[Candidate, fastui_form(Candidate)]):
    new_cand = Candidate(**form.model_dump())
    txt_cand = new_cand.cand_skills
    data.post_candidate(txt_cand)

    return [c.FireEvent(event=GoToEvent(url='/candidate/'))]


@app.get('/api/candi_skills/', response_model=FastUI, response_model_exclude_none=True)
def add_pair_page():
    txt_cand = data.get_candidate()
    return [
        c.Page(
            components=[
                c.Heading(text='Знания и умения кандидата:', level=1),
                c.Heading(text='[' + txt_cand + ']', level=3),
                c.ModelForm(
                    model=Candidate,
                    submit_url='/api/candi/'),
                c.Markdown(

                    text="""\
    ________________________________________________________________________________________
    Введите знания и умения кандидата, разделенные пробелами
    """
                ),

                c.Link(components=[c.Text(text='Назад к предыдущему режиму')], on_click=BackEvent()),
            ]
        )
    ]


@app.get('/api/skill_chain/', response_model=FastUI, response_model_exclude_none=True)
def skill_ebz_chain() -> list[AnyComponent]:
    txt_cand = data.get_candidate()
    chain_lst = []
    for s in txt_cand.split():
        cur = []
        i = s
        while i in dct:
            cur.append(i)
            i = dct[i]
        if cur:
            chain_lst.append(SkillChain(skill=s, chain='->'.join(cur)))
        else:
            chain_lst.append(SkillChain(skill=s, chain='Not in EBZ'))
    return [
        c.Page(  # Page provides a basic container for components
            components=[
                c.Heading(text='Кандидат -> Единая база знаний', level=1),
                c.Table(
                    data=chain_lst,
                    columns=[
                        DisplayLookup(field='skill', table_width_percent=20),
                        DisplayLookup(field='chain', table_width_percent=50),
                    ],
                ),
                c.Div(
                    components=[
                        # c.Heading(text='________________________________', level=3),
                        c.Markdown(

                            text="""\
    ________________________________________________________________________________________
    Слева навыки кандидата (skills).
    Если они есть в EBZ, то справа цепочка элементов ЕБЗ (chain).
    Если нет, то "Not in EBZ"
    """
                        ),
                        c.Link(components=[c.Text(text='Назад к предыдущему режиму')], on_click=BackEvent()),
                    ]
                ),
            ]
        ),
    ]


@app.get('/{path:path}')
async def html_landing() -> HTMLResponse:
    """Simple HTML page which serves the React app, comes last as it matches all paths."""
    return HTMLResponse(prebuilt_html(title='FastUI Demo'))