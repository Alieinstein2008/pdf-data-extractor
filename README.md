# PDF Data Extractor

Automação desenvolvida em Python para extrair dados estruturados de documentos PDF e consolidá-los em planilhas Excel, reduzindo o trabalho manual de consulta e organização de informações.

O projeto foi desenvolvido para apoiar uma atividade operacional envolvendo documentos obtidos por meio do Sistema Nacional de Informações de Defesa do Consumidor, integrado ao Procon-MPMG.

## Visão geral

O PDF Data Extractor automatiza o fluxo de processamento de documentos, desde a identificação dos arquivos de entrada até a geração de uma planilha consolidada.

```text
Documentos PDF
      |
      v
Extração de dados
      |
      v
Processamento em lote
      |
      v
Consolidação dos registros
      |
      v
Planilha Excel
```

### Funcionalidades

- **Leitura em lote:** processamento de múltiplos arquivos PDF a partir de um diretório de entrada.
- **Extração estruturada:** coleta de informações presentes nos documentos, incluindo dados de tabelas e metadados esperados.
- **Consolidação de dados:** organização dos registros extraídos em uma estrutura tabular.
- **Exportação para Excel:** geração de uma planilha com os dados processados.
- **Tratamento de erros por documento:** identificação de falhas de extração sem interromper o processamento dos arquivos seguintes.

## Tecnologias

| Tecnologia | Aplicação no projeto |
|---|---|
| Python | Linguagem utilizada na implementação da automação. |
| [pdfplumber](https://github.com/jsvine/pdfplumber) | Extração de informações de documentos PDF. |
| [pandas](https://pandas.pydata.org/) | Estruturação e consolidação dos dados extraídos. |
| [openpyxl](https://openpyxl.readthedocs.io/) | Geração e manipulação de planilhas Excel. |

## Arquitetura e organização

O projeto separa a extração dos documentos, o processamento em lote e a geração dos arquivos de saída em módulos específicos.

```text
pdf-data-extractor/
├── src/
│   ├── main.py
│   ├── extraction/
│   │   ├── pdf_extractor.py
│   │   ├── extraction_config.py
│   │   └── extraction_error.py
│   ├── processing/
│   │   └── batch_processor.py
│   └── output/
│       └── excel_writer.py
├── data/
│   └── input/
├── output/
├── .gitignore
├── README.md
└── requirements.txt
```

### Responsabilidades dos módulos

- `main.py`: ponto de entrada para execução do processo.
- `extraction/`: reúne os componentes relacionados à extração, às configurações e aos erros específicos.
- `processing/batch_processor.py`: coordena o processamento dos documentos em lote.
- `output/excel_writer.py`: concentra a responsabilidade de gerar a planilha Excel.
- `data/input/`: diretório destinado aos documentos de entrada.
- `output/`: diretório de saída dos resultados.

Essa organização delimita as responsabilidades principais e facilita a manutenção dos componentes envolvidos no fluxo de extração.

## Instalação

### Pré-requisitos

- Python instalado.
- Git instalado.
- Documentos PDF compatíveis com a estrutura de extração implementada.

Clone o repositório:

```bash
git clone https://github.com/Alieinstein2008/pdf-data-extractor.git
cd pdf-data-extractor
```

Crie um ambiente virtual:

```bash
python -m venv .venv
```

Ative o ambiente virtual no Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

## Utilização

### 1. Adicione os documentos

Coloque os arquivos PDF que deseja processar no diretório:

```text
data/input/
```

### 2. Execute a automação

Na raiz do repositório, execute:

```bash
python src/main.py
```

### 3. Consulte os resultados

Após o processamento, os registros extraídos são consolidados na planilha:

```text
output/tabela.xlsx
```

## Tratamento de erros

A automação identifica falhas relacionadas à estrutura ou aos metadados esperados de cada documento. Quando um arquivo apresenta um problema, o erro é registrado e o processamento continua com os demais arquivos.

Exemplo de saída:

```text
Processando: documento-01.pdf...
OK — 42 registros extraídos.

Processando: documento-02.pdf...
ERRO — documento-02.pdf: Metadado não encontrado: Guia Nº:

Processando: documento-03.pdf...
OK — 31 registros extraídos.
```

Nesse cenário, a falha do segundo documento não impede a extração dos registros dos demais arquivos processáveis.

## Limitações e considerações

O extrator foi desenvolvido para documentos que seguem uma estrutura específica. Alterações na disposição das informações, nos metadados ou na nomenclatura dos campos podem exigir ajustes nas configurações ou na lógica de extração.

Os arquivos PDF de entrada e as planilhas geradas são mantidos fora do versionamento por meio das regras definidas em `.gitignore`.

## Finalidade do projeto

O PDF Data Extractor foi desenvolvido como ferramenta de apoio operacional para automatizar a extração e a organização de informações utilizadas em atividades de análise, estudos e pesquisas.

Seu foco é reduzir tarefas manuais repetitivas e padronizar a consolidação dos dados, mantendo a geração dos resultados em uma planilha estruturada. O projeto possui finalidade operacional e acadêmica, não sendo destinado à comercialização das informações processadas.
