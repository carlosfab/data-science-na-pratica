[<img src="assets/dsnp_banner.png" alt="Data Science na Prática | https://sigmoidal.ai)" title="Data Science na Prática | https://sigmoidal.ai)"/>](https://sigmoidal.ai/)

<div align="center">
  
  [![Linkedin Badge](https://img.shields.io/badge/LinkedIn-0077B5?style=flat-square&logo=Linkedin&logoColor=white&link=https://www.linkedin.com/in/carlos-melo-data-science/)](https://www.linkedin.com/in/carlos-melo-data-science/)
  [![YouTube Badge](https://img.shields.io/badge/YouTube-FF0000?style=flat-square&logo=youtube&logoColor=white)](https://www.youtube.com/@CarlosMeloSigmoidal)
  [![Instagram Badge](https://img.shields.io/badge/Instagram-E4405F?style=flat-square&logo=instagram&logoColor=white)](https://www.instagram.com/carlos_melo.py)
  [![Twitter Badge](https://img.shields.io/twitter/follow/:carlos_melo_py)](https://twitter.com/carlos_melo_py)

</div>

# Data Science na Prática

Este repositório é dedicado ao treinamento "Data Science na Prática". Siga os passos abaixo para configurar o ambiente de desenvolvimento local e instalar as dependências utilizadas durante as aulas.

## Pré-requisitos

* **Google Colab** - Plataforma baseada em nuvem que permite a execução de notebooks Jupyter sem a necessidade de configuração. [Crie sua conta no Google Colab](https://colab.research.google.com/signup)

* **VSCode** - Editor de código utilizado durante o treinamento. Disponível para Windows, macOS e Linux. [Instalação oficial do VSCode](https://code.visualstudio.com/download)

* **Pyenv** - Ferramenta para gerenciar múltiplas versões do Python. A versão recomendada do Python para este projeto é a `3.11.3`. [Instruções oficiais de instalação do Pyenv](https://github.com/pyenv/pyenv#installation)

* **Poetry** - Ferramenta de gerenciamento de dependências em Python. [Instruções oficiais de instalação do Poetry](https://python-poetry.org/docs/#installation)

* **Git** - Ferramenta de controle de versão distribuído. [Instruções oficiais de instalação do Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

* **GitHub** - Plataforma de hospedagem de código. É essencial ter uma conta para interagir com os repositórios. [Como criar uma conta no GitHub](https://docs.github.com/pt/get-started/onboarding/getting-started-with-your-github-account)

## Instalação e Configuração

Aqui está um resumo dos passos que você precisa seguir:

1. Clonar o [Repositório Github](https://github.com/carlosfab/data-science-na-pratica) para a sua máquina local e acessar a pasta `data-science-na-pratica`:

   ```bash
   git clone https://github.com/carlosfab/data-science-na-pratica.git
   cd data-science-na-pratica
   ```

2. Configurar o Poetry para criar ambientes virtuais dentro do diretório do projeto.

   ```bash
   poetry config virtualenvs.in-project true
   ```

3. Configurar a versão `3.11.3` do Python com Pyenv:

   ```bash
   pyenv install 3.11.3
   pyenv local 3.11.3
   ```

4. Instalar as dependências do projeto:

   ```bash
   poetry install
   ```

5. Ativar o ambiente virtual.

   ```bash
   poetry shell
   ```

6. Testando sua instalação

   Após seguir os passos de instalação e configuração, execute os testes para garantir que tudo está funcionando como esperado:

   ```bash
   task test
   ```

## **🚀 Módulos do DSNP**

| Módulo | Descrição | Link |
|--------|-----------|----------------------|
| **1 - Introdução ao Data Sciece** | Apresentação do conteúdo do curso, conceitos fundamentais da Ciência de Dados e *Data-driven Decisions*. | [Módulo 1](notebooks/01_introducao_ao_data_science) |
| **2 - Análise e Exploração de Dados** | Aprenda a importar dados, fazer a limpeza e extrair informações relevantes usando a biblioteca `pandas`. | [Módulo 2](notebooks/02_analise_e_exploracao_de_dados) |
| **3 - Visualização de Dados** | Aprenda a criar visualizações informativas e impactantes com `matplotlib`. | [Módulo 3](notebooks/03_visualizacao_de_dados/) |
| **4 - Data Storytelling** | Conte histórias com dados, e aumente o impacto do seu trabalho. | [Módulo 4](notebooks/04_data_storytelling/) |
| **5 - Introdução ao Machine Learning** | Aprenda Machine Learning do zero. | [Módulo 5](notebooks/05_intro_ao_machine_learning/) |
| **6 - Machine Learning Avançado** | Aplicações e técnicas avançadas de Machine Learning. | [Módulo 6](notebooks/06_machine_learning_avancado/) |
| **7 - Auto Machine Learning** | Ganhe tempo e performance com Auto Machine Learning. | [Módulo 7](notebooks/07_auto_machine_learning/) |
| **8 - Criando um Projeto do Zero** | Construa um projeto real completo, da ideia à solução. | [Módulo 8](notebooks/08_projeto_do_zero/) |
| **9 - Deploy de Aplicações de Machine Learning** | Coloque seu modelo em Produção. | [Módulo 9](notebooks/09_deploy/) |
| **10 - Deep Learning** | Aprenda a utilizar ténicas de Deep Learning. | [Módulo 10](notebooks/10_deep_learning/) |

## 🚀 Projetos

# TODO

## Sobre os Instrutores

<p align="left">
Carlos Melo é <strong>Engenheiro de Visão Computacional</strong> com formação em Ciências Aeronáuticas pela Academia da Força Aérea e <strong>Mestrado em Engenharia Aeroespacial</strong> pelo Instituto Tecnológico de Aeronáutica (ITA).
</p>

<p align="left">
[Rafael Duarte](https://github.com/rafaelnduarte) é <strong>Cientista de Dados, Colaborador e especialista em Marketing Analytics no Sigmoidal</strong>. Formado em Ciência de Dados, com <strong>MBA e Master's em Big Data e Business Intelligence</strong>.
</p>
