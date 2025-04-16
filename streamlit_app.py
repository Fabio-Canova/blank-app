import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

#import os
#st.write(os.path.abspath('.streamlit/secrets.toml'))
#st.write(st.secrets)

st.set_page_config(page_title="VICTORIA ESTUDO DE ESTOQUE", layout="wide")
###########################################################
################### SEGURANÇA #############################
def check_password():
    """Verifica se o usuário digitou a senha correta."""
    
    def password_entered():
        """Verifica se a senha corresponde a algum usuário."""
        if st.session_state["user"] in st.secrets.passwords:
            if st.session_state["password"] == st.secrets.passwords[st.session_state["user"]]:
                st.session_state["password_correct"] = True
                del st.session_state["password"]  # Não armazena a senha
                del st.session_state["user"]
            else:
                st.session_state["password_correct"] = False
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # Mostra o formulário de login
        st.text_input("Usuário", key="user")
        st.text_input("Senha", type="password", key="password")
        st.button("Entrar", on_click=password_entered)
        return False
    elif not st.session_state["password_correct"]:
        # Se a senha estiver errada, mostra o formulário novamente + mensagem de erro
        st.text_input("Usuário", key="user")
        st.text_input("Senha", type="password", key="password")
        st.button("Entrar", on_click=password_entered)
        st.error("Usuário ou senha incorretos")
        return False
    else:
        # Senha correta
        return True

if check_password():
    st.success("Login efetuado com sucesso!")
    st.title("VICTORIA ESTUDO DE ESTOQUE")
    
    ###########################################################
    ################### APP AQUI ##############################

    # Configuração da página
    #st.set_page_config(page_title="VICTORIA ESTUDO DE ESTOQU", layout="wide")


    # Função para remover ou substituir caracteres indesejados
    def importar_CSV(caminho_arquivo):

        df = pd.read_csv(caminho_arquivo,
                                    sep=";",  # Delimitador usado no CSV
                                    header = 0,
                                    encoding="utf-8",  # Define a codificação do arquivo
                                    na_values=["<Nenhum>","NaN","N/A", "", "NULL"],  # Considera "NaN", valores vazios e "NULL" como NaN
                                    encoding_errors='replace',
                                    on_bad_lines="skip",
                                    keep_default_na=False,  # Ignora os valores padrão do Pandas para NaN
                                    na_filter=True,  # Mantém a detecção de NaN ativada
                                    skip_blank_lines=False,  # Mantém as linhas em branco
                                    low_memory=False,  # Habilita leitura em pedaços menores para economizar memória
                                    memory_map=True  # Usa mapeamento de memória para leitura mais rápida
        ) #Elementos
        df.fillna("")

        # Retorna o DataFrame com os dados limpos
        return df

    #Aux_Base_Date = pd.read_csv(
    #    "data/Aux_Base_Date.txt",
    #    delimiter=';',
    #    quotechar='"',
    #    encoding='utf-8',
    #    engine='python',
    #    on_bad_lines='warn'  # Avisa se encontrar linhas problemáticas
    #)




    # Carregar os CSVs como DataFrames
    #@st.cache_data
    def load_table_1():
        # Carrega a primeira tabela
        Etiqueta="data/Etiqueta.txt"
        return importar_CSV(Etiqueta)

    #@st.cache_data
    def load_table_2():
        # Carrega a segunda tabela
        Exporta_01="data/Exporta_01.txt"
        return importar_CSV(Exporta_01)

    #@st.cache_data
    def load_table_3():
        # Carrega a segunda tabela
        Exporta_02="data/Exporta_02.txt"
        return importar_CSV(Exporta_02)

    #@st.cache_data
    def load_table_4():
        # Carrega a segunda tabela
        Exporta_03="data/Exporta_03.txt"
        return importar_CSV(Exporta_03)

    #@st.cache_data
    def load_table_5():
        # Carrega a segunda tabela
        Nomenclatura_Producao="data/Nomenclatura_Produção.txt"
        return importar_CSV(Nomenclatura_Producao)

    #@st.cache_data
    def load_table_6():
        # Carrega a segunda tabela
        Aux_Base_Date="data/Aux_Base_Date.txt"
        return importar_CSV(Aux_Base_Date)

    #@st.cache_data
    def load_table_7():
        # Carrega a segunda tabela
        Balanco_AU000001="data/Balanco_AU000001.txt"
        return importar_CSV(Balanco_AU000001)

    #@st.cache_data
    def load_table_8():
        # Carrega a segunda tabela
        Aux_Estoque="data/Aux_Estoque.txt"
        return importar_CSV(Aux_Estoque)



    # Carrega as tabelas
    df_Etiqueta = load_table_1()
    df_Exporta_01 = load_table_2()
    df_Exporta_02 = load_table_3()
    df_Exporta_03 = load_table_4()
    df_Nomenclatura_Producao = load_table_5()
    df_Aux_Base_Date = load_table_6()
    df_Balanco_AU000001 = load_table_7()
    df_Aux_Estoque = load_table_8()


    #################################################################################################################################
    ############### TRABALHO ETIQUETA ###############################################################################################
    #Reduz as Colunas
    df_Etiqueta_Red = df_Etiqueta[['ETIQUETA', 'PRODUTO', 'QTDE','peso','DATA DO PEDIDO','ENCERRAMENTO','valor metal','val out metais','val pedras','val servi�os','opera��o']]
    df_Etiqueta_Red = df_Etiqueta_Red[df_Etiqueta_Red['opera��o'] != 'CANCELA PRODUÇÃO']

    #renomeia
    df_Etiqueta_Red = df_Etiqueta_Red.rename(columns={'val servi�os': 'val servicos'})

    #trabalha a data do pedido
    # Converter para datetime
    df_Etiqueta_Red['data_pedido'] = pd.to_datetime(
        df_Etiqueta_Red['DATA DO PEDIDO'],
        format='%d/%m/%Y %H:%M:%S',  # Formato dia/mês/ano hora:minuto:segundo
        errors='coerce'  # Converte erros para NaT (valores vazios)
    )
    # Extrair o mês (1 a 12)
    df_Etiqueta_Red['mes_pedido'] = df_Etiqueta_Red['data_pedido'].dt.month
    df_Etiqueta_Red['ano_pedido'] = df_Etiqueta_Red['data_pedido'].dt.year

    # Aplicando na coluna ENCERRAMENTO
    df_Etiqueta_Red['ENCERRAMENTO'] = df_Etiqueta_Red['ENCERRAMENTO'].str.replace(r'\s*/\s*/\s*', '', regex=True)

    # Passo 2: Converter para data (formato dd/mm/aaaa)
    df_Etiqueta_Red['data_encerramento'] = pd.to_datetime(
        df_Etiqueta_Red['ENCERRAMENTO'],
        format='%d/%m/%Y',
        errors='coerce'
    )

    # Extraindo mês e ano (apenas para datas válidas)
    df_Etiqueta_Red['mes_encerramento'] = df_Etiqueta_Red['data_encerramento'].dt.month
    df_Etiqueta_Red['ano_encerramento'] = df_Etiqueta_Red['data_encerramento'].dt.year

    # Converte numericos
    df_Etiqueta_Red['peso_corr'] = df_Etiqueta_Red['peso'].str.replace(',', '.').astype(float)
    df_Etiqueta_Red['valor_metal_corr'] = df_Etiqueta_Red['valor metal'].str.replace(',', '.').astype(float)
    df_Etiqueta_Red['valor_out_corr'] = df_Etiqueta_Red['val out metais'].str.replace(',', '.').astype(float)
    df_Etiqueta_Red['valor_pedras_corr'] = df_Etiqueta_Red['val pedras'].str.replace(',', '.').astype(float)
    df_Etiqueta_Red['valor_servicos_corr'] = df_Etiqueta_Red['val servicos'].str.replace(',', '.').astype(float)



    ########################################################################################################################
    ############### SALDO EM ABERTO FINAL DO MES ###########################################################################
    df_Etiqueta_pedidos_Ag = df_Etiqueta_Red.groupby(['ano_pedido','mes_pedido'], as_index=False).agg(
        ped_peso_corr=('peso_corr', 'sum'),
        ped_valor_metal_corr=('valor_metal_corr', 'sum'),
        ped_valor_out_corr=('valor_out_corr', 'sum'),
        ped_valor_pedras_corr=('valor_pedras_corr', 'sum'),
        ped_valor_servicos_corr=('valor_servicos_corr', 'sum')
    ).sort_values(['ano_pedido','mes_pedido'])

    df_Etiqueta_fabricados_Ag = df_Etiqueta_Red.groupby(['ano_encerramento','mes_encerramento'], as_index=False).agg(
        fab_peso_corr=('peso_corr', 'sum'),
        fab_valor_metal_corr=('valor_metal_corr', 'sum'),
        fab_valor_out_corr=('valor_out_corr', 'sum'),
        fab_valor_pedras_corr=('valor_pedras_corr', 'sum'),
        fab_valor_servicos_corr=('valor_servicos_corr', 'sum')
    ).sort_values(['ano_encerramento','mes_encerramento'])

    #junta
    df_Etiqueta_abertos = df_Etiqueta_pedidos_Ag.merge(
            df_Etiqueta_fabricados_Ag,
            left_on=["ano_pedido", "mes_pedido"],
            right_on=["ano_encerramento", "mes_encerramento"],
            how="left"
    )

    #cria saldos
    df_Etiqueta_abertos['peso_corr'] = df_Etiqueta_abertos.get('ped_peso_corr', 0) - df_Etiqueta_abertos.get('fab_peso_corr', 0)
    df_Etiqueta_abertos['valor_metal_corr'] = df_Etiqueta_abertos.get('ped_valor_metal_corr', 0) - df_Etiqueta_abertos.get('fab_valor_metal_corr', 0)
    df_Etiqueta_abertos['valor_out_corr'] = df_Etiqueta_abertos.get('ped_valor_out_corr', 0) - df_Etiqueta_abertos.get('fab_valor_out_corr', 0)
    df_Etiqueta_abertos['valor_pedras_corr'] = df_Etiqueta_abertos.get('ped_valor_pedras_corr', 0) - df_Etiqueta_abertos.get('fab_valor_pedras_corr', 0)
    df_Etiqueta_abertos['valor_servicos_corr'] = df_Etiqueta_abertos.get('ped_valor_servicos_corr', 0) - df_Etiqueta_abertos.get('fab_valor_servicos_corr', 0)

    df_Etiqueta_abertos = df_Etiqueta_abertos.sort_values(['ano_pedido', 'mes_pedido'])

    # Calculando os acumulados por grupo de estoque
    df_Etiqueta_abertos['acum_peso_corr'] = df_Etiqueta_abertos['peso_corr'].cumsum()
    df_Etiqueta_abertos['acum_valor_metal_corr'] = df_Etiqueta_abertos['valor_metal_corr'].cumsum()
    df_Etiqueta_abertos['acum_valor_out_corr'] = df_Etiqueta_abertos['valor_out_corr'].cumsum()
    df_Etiqueta_abertos['acum_valor_pedras_corr'] = df_Etiqueta_abertos['valor_pedras_corr'].cumsum()
    df_Etiqueta_abertos['acum_valor_servicos_corr'] = df_Etiqueta_abertos['valor_servicos_corr'].cumsum()


    #reduz colunas
    df_Etiqueta_abertos = df_Etiqueta_abertos[['mes_pedido','ano_pedido','ped_peso_corr','ped_valor_metal_corr','ped_valor_out_corr','ped_valor_pedras_corr','ped_valor_servicos_corr','fab_peso_corr','fab_valor_metal_corr','fab_valor_out_corr','fab_valor_pedras_corr','fab_valor_servicos_corr','acum_peso_corr','acum_valor_metal_corr','acum_valor_out_corr','acum_valor_pedras_corr','acum_valor_servicos_corr']]
    df_Etiqueta_abertos['mes_ano_pedido'] = df_Etiqueta_abertos['ano_pedido'].astype(str) + '-' + df_Etiqueta_abertos['mes_pedido'].astype(str).str.zfill(2)



    #########################################################################################################
    ############### TRABALHO NOMENCLATURA ###################################################################
    df_Nomenclatura_Producao= df_Nomenclatura_Producao[['produto', 'insumo', 'descri��o insumo','tipo','qtd','peso','custo','total','mup','valor mup']]

    #renomeia
    df_Nomenclatura_Producao = df_Nomenclatura_Producao.rename(columns={'descri��o insumo': 'descricao insumo'})

    #junta
    df_Etiqueta_Det= df_Etiqueta_Red.merge(
            df_Nomenclatura_Producao,
            left_on=["PRODUTO"],
            right_on=["produto"],
            how="left"
    )

    #filtra
    df_Etiqueta_Det = df_Etiqueta_Det[df_Etiqueta_Det['tipo'] == 'INSUMO']

    df_Etiqueta_Det['qtd_insumo'] = df_Etiqueta_Det['qtd'].str.replace(',', '.').astype(float)
    df_Etiqueta_Det['peso_y'] = df_Etiqueta_Det['peso_y'].str.replace(',', '.').astype(float)
    df_Etiqueta_Det["custo_insumo"] = (
        df_Etiqueta_Det["custo"]
        .str.replace("R\$", "", regex=True)  # Remove "R$"
        .str.replace(".", "", regex=False)   # Remove pontos (milhares)
        .str.replace(",", ".", regex=False)  # Substitui vírgula por ponto
        .astype(float)
    )
    df_Etiqueta_Det["total_insumo"] = (
        df_Etiqueta_Det["total"]
        .str.replace("R\$", "", regex=True)  # Remove "R$"
        .str.replace(".", "", regex=False)   # Remove pontos (milhares)
        .str.replace(",", ".", regex=False)  # Substitui vírgula por ponto
        .astype(float)
    )

    #reduz colunas
    df_Etiqueta_Det= df_Etiqueta_Det[['ETIQUETA', 'PRODUTO', 'QTDE','data_pedido','mes_pedido','ano_pedido','data_encerramento','mes_encerramento','ano_encerramento','peso_corr','insumo','descricao insumo','peso_y','qtd_insumo','custo_insumo','total_insumo']]


    #Agrupa por mes
    df_Etiqueta_Det_ped_Ag = df_Etiqueta_Det.groupby(['ano_pedido','mes_pedido'], as_index=False).agg(
        ped_qtd_insumo=('qtd_insumo', 'sum')
    ).sort_values(['ano_pedido','mes_pedido'])

    df_Etiqueta_Det_fab_Ag = df_Etiqueta_Det.groupby(['ano_encerramento','mes_encerramento'], as_index=False).agg(
        ped_qtd_insumo=('qtd_insumo', 'sum')
    ).sort_values(['ano_encerramento','mes_encerramento'])

    #junta
    df_Etiqueta_Det_Ag = df_Etiqueta_Det_ped_Ag.merge(
            df_Etiqueta_Det_fab_Ag,
            left_on=["ano_pedido", "mes_pedido"],
            right_on=["ano_encerramento", "mes_encerramento"],
            how="left"
    )

    #reduz colunas
    df_Etiqueta_Det_Ag = df_Etiqueta_Det_Ag[['mes_pedido','ano_pedido','ped_qtd_insumo_x','ped_qtd_insumo_y']]
    df_Etiqueta_Det_Ag['mes_ano_pedido'] = df_Etiqueta_Det_Ag['ano_pedido'].astype(str) + '-' + df_Etiqueta_abertos['mes_pedido'].astype(str).str.zfill(2)

    #renomeia
    df_Etiqueta_Det_Ag = df_Etiqueta_Det_Ag.rename(columns={'ped_qtd_insumo_x': 'insumo_ped'})
    df_Etiqueta_Det_Ag = df_Etiqueta_Det_Ag.rename(columns={'ped_qtd_insumo_y': 'insumo_fab'})



    ########################################################################################################################
    ############### SALDO EM ABERTO FINAL DO MES ###########################################################################
    #cria saldos
    df_Etiqueta_Det_Ag['insumos_aberto'] = df_Etiqueta_Det_Ag.get('insumo_ped', 0) - df_Etiqueta_Det_Ag.get('insumo_fab', 0)

    df_Etiqueta_Det_Ag = df_Etiqueta_Det_Ag.sort_values(['ano_pedido', 'mes_pedido'])

    # Calculando os acumulados por grupo de estoque
    df_Etiqueta_Det_Ag['acum_insumos_aberto'] = df_Etiqueta_Det_Ag['insumos_aberto'].cumsum()



    #########################################################################################################
    ############### JUNTA TUDO POR MES ######################################################################

    df_Etiqueta_geral = df_Etiqueta_abertos.merge(
            df_Etiqueta_Det_Ag,
            left_on=["ano_pedido", "mes_pedido"],
            right_on=["ano_pedido", "mes_pedido"],
            how="left"
    )

    df_Etiqueta_geral = df_Etiqueta_geral[['mes_ano_pedido_x','mes_pedido','ano_pedido','ped_peso_corr','ped_valor_metal_corr','ped_valor_out_corr','ped_valor_pedras_corr','ped_valor_servicos_corr','fab_peso_corr','fab_valor_metal_corr','fab_valor_out_corr','fab_valor_pedras_corr','fab_valor_servicos_corr','acum_peso_corr','acum_valor_metal_corr','acum_valor_out_corr','acum_valor_pedras_corr','acum_valor_servicos_corr','insumo_ped','insumo_fab','insumos_aberto','acum_insumos_aberto']]





    #########################################################################################################
    ############### BALANCO #################################################################################
    # Supondo que você tenha 3 DataFrames: df1, df2 e df3
    Balanco_AU000007_3 = pd.concat([df_Exporta_01, df_Exporta_02, df_Exporta_03], ignore_index=True)
    Balanco_AU000007_3= Balanco_AU000007_3[['data', 'estoque', 'opera��o','entra(q)','sa�da(q)','saldo(q)']]
    Balanco_AU000007_1 = Balanco_AU000007_3[Balanco_AU000007_3['opera��o'] != 'Saldo Anterior']


    #pega os saldos iniciais
    Balanco_AU000007_inicial = Balanco_AU000007_3.loc[[0]]

    Balanco_AU000007_inicial['saldo(q)'] = Balanco_AU000007_inicial['saldo(q)'].str.replace(',', '.').astype(float)
    Balanco_AU000007_inicial['entra(q)'] = Balanco_AU000007_inicial['entra(q)'].str.replace(',', '.').astype(float)
    Balanco_AU000007_inicial['sa�da(q)'] = Balanco_AU000007_inicial['sa�da(q)'].str.replace(',', '.').astype(float)
    Balanco_AU000007_inicial['entrada'] = Balanco_AU000007_inicial['saldo(q)']-Balanco_AU000007_inicial['entra(q)']+Balanco_AU000007_inicial['sa�da(q)']

    Balanco_AU000007_inicial = Balanco_AU000007_inicial.rename(columns={'sa�da(q)': 'saida'})
    Balanco_AU000007_inicial['operacao'] = "Saldo Inicial Calculado"
    Balanco_AU000007_inicial= Balanco_AU000007_inicial[['data', 'estoque', 'operacao','entrada','saida']]

    #renomeia
    Balanco_AU000007_1 = Balanco_AU000007_1.rename(columns={'entra(q)': 'ent'})
    Balanco_AU000007_1 = Balanco_AU000007_1.rename(columns={'sa�da(q)': 'sai'})
    Balanco_AU000007_1 = Balanco_AU000007_1.rename(columns={'opera��o': 'operacao'})

    Balanco_AU000007_1['entrada'] = Balanco_AU000007_1['ent'].str.replace(',', '.').astype(float)
    Balanco_AU000007_1['saida'] = Balanco_AU000007_1['sai'].str.replace(',', '.').astype(float)

    Balanco_AU000007_1= Balanco_AU000007_1[['data', 'estoque', 'operacao','entrada','saida']]
    Balanco_AU000007 = pd.concat([Balanco_AU000007_inicial, Balanco_AU000007_1], ignore_index=True)

    #trabalha a data do pedido
    # Converter para datetime
    Balanco_AU000007['data_corr'] = pd.to_datetime(
        Balanco_AU000007['data'],
        format='%d/%m/%Y',
        errors='coerce'
    )


    #print(Balanco_AU000007.head(30))
    #print(Balanco_AU000007_inicial.head(30))
    #print(df_Exporta_01.head(30))
    #print(df_Exporta_02.head(30))
    #print(df_Exporta_03.head(30))
    # Ordenando por estoque e data (para garantir a ordem correta)
    Balanco_AU000007 = Balanco_AU000007.sort_values(['data_corr'])



    ##########################################################################################
    ######################logica por mes
    # Extraindo mês e ano (apenas para datas válidas)
    Balanco_AU000007['mes_data'] = Balanco_AU000007['data_corr'].dt.month
    Balanco_AU000007['ano_data'] = Balanco_AU000007['data_corr'].dt.year

    Balanco_AU000007_ag_mes = Balanco_AU000007.groupby(['ano_data','mes_data'], as_index=False).agg(
        entrada=('entrada', 'sum'),
        saida=('saida', 'sum')
    ).sort_values(['ano_data','mes_data'])

    # Supondo que 'resultado' seja o DataFrame obtido na etapa anterior
    # Ordenando por estoque e data (para garantir a ordem correta)
    Balanco_AU000007_ag_mes = Balanco_AU000007_ag_mes.sort_values(['ano_data','mes_data'])

    # Calculando os acumulados por grupo de estoque e dia de movimentacao
    Balanco_AU000007_ag_mes['entrada_acumulada'] = Balanco_AU000007_ag_mes['entrada'].cumsum()
    Balanco_AU000007_ag_mes['saida_acumulada'] = Balanco_AU000007_ag_mes['saida'].cumsum()

    # Calculando o saldo mensal acumulado
    Balanco_AU000007_ag_mes['saldo_acumulado'] = Balanco_AU000007_ag_mes['entrada_acumulada'] - Balanco_AU000007_ag_mes['saida_acumulada']





    #######################################################################################################################
    #######################################################################################################################
    ################################ COMEÇA O RELATORIO ###################################################################

    ###### CRIA GRAFICO DOS PESOS DE PEDIDOS E PESOS ENTREGUES
    # 1. Criar colunas de mês/ano formatadas para melhor exibição
    df_Etiqueta_Red['mes_ano_pedido'] = df_Etiqueta_Red['ano_pedido'].astype(str) + '-' + df_Etiqueta_Red['mes_pedido'].astype(str).str.zfill(2)
    df_Etiqueta_Red['mes_ano_encerramento'] = df_Etiqueta_Red['ano_encerramento'].astype(str) + '-' + df_Etiqueta_Red['mes_encerramento'].astype(str).str.zfill(2)

    # 2. Agregar os dados por mês/ano
    df_pedido_mensal = df_Etiqueta_Red.groupby('mes_ano_pedido', as_index=False)['peso_corr'].sum()
    df_encerramento_mensal = df_Etiqueta_Red.groupby('mes_ano_encerramento', as_index=False)['peso_corr'].sum()

    #### GRAFICO 1 ########
    # 1. Criar figura com eixo Y secundário
    fig4 = make_subplots(specs=[[{"secondary_y": True}]])

    # 2. Adicionar barras para ped_peso_corr e fab_peso_corr (eixo Y primário)
    fig4.add_trace(
        go.Bar(
            x=df_Etiqueta_geral['mes_ano_pedido_x'],
            y=df_Etiqueta_geral['ped_peso_corr'],
            name='Peso Pedido',
            marker_color='#1f77b4'  # Azul
        ),
        secondary_y=False
    )

    fig4.add_trace(
        go.Bar(
            x=df_Etiqueta_geral['mes_ano_pedido_x'],
            y=df_Etiqueta_geral['fab_peso_corr'],
            name='Peso Fabricado',
            marker_color='#ff7f0e'  # Laranja
        ),
        secondary_y=False
    )

    # 3. Adicionar linha para acum_peso_corr (eixo Y secundário)
    fig4.add_trace(
        go.Scatter(
            x=df_Etiqueta_geral['mes_ano_pedido_x'],
            y=df_Etiqueta_geral['acum_peso_corr'],
            name='Em Aberto',
            line=dict(color='#2ca02c', width=3),  # Verde
            mode='lines+markers'
        ),
        secondary_y=True
    )

    # 4. Configurar layout
    fig4.update_layout(
        title='Peso: Pedido vs Fabricado com Em aberto',
        xaxis_title='Mês/Ano',
        yaxis_title='Peso (kg)',
        yaxis2_title='Peso em Aberto (kg)',
        barmode='group',  # Barras agrupadas lado a lado
        template='plotly_white'
    )

    # 5. Ajustar eixos Y
    fig4.update_yaxes(title_text="Peso (kg)", secondary_y=False)
    fig4.update_yaxes(title_text="Peso em Aberto (kg)", secondary_y=True)


    #### GRAFICO 2 ########
    # 1. Criar figura com eixo Y secundário
    fig2 = make_subplots(specs=[[{"secondary_y": True}]])

    # 2. Adicionar barras para ped_peso_corr e fab_peso_corr (eixo Y primário)
    fig2.add_trace(
        go.Bar(
            x=df_Etiqueta_geral['mes_ano_pedido_x'],
            y=df_Etiqueta_geral['insumo_ped'],
            name='Insumos Pedido',
            marker_color='#1f77b4'  # Azul
        ),
        secondary_y=False
    )

    fig2.add_trace(
        go.Bar(
            x=df_Etiqueta_geral['mes_ano_pedido_x'],
            y=df_Etiqueta_geral['insumo_fab'],
            name='Insumos Fabricado',
            marker_color='#ff7f0e'  # Laranja
        ),
        secondary_y=False
    )

    # 3. Adicionar linha para acum_peso_corr (eixo Y secundário)
    fig2.add_trace(
        go.Scatter(
            x=df_Etiqueta_geral['mes_ano_pedido_x'],
            y=df_Etiqueta_geral['acum_insumos_aberto'],
            name='Em Aberto',
            line=dict(color='#2ca02c', width=3),  # Verde
            mode='lines+markers'
        ),
        secondary_y=True
    )

    # 4. Configurar layout
    fig2.update_layout(
        title='Insumos: Pedido vs Fabricado com Em aberto',
        xaxis_title='Mês/Ano',
        yaxis_title='Insumo (Qtd))',
        yaxis2_title='Insumos em Aberto (Qtd)',
        barmode='group',  # Barras agrupadas lado a lado
        template='plotly_white'
    )

    # 5. Ajustar eixos Y
    fig2.update_yaxes(title_text="Insumo (Qtd)", secondary_y=False)
    fig2.update_yaxes(title_text="Insumo em Aberto (Qtd)", secondary_y=True)


    # 6. Exibição lado a lado no Streamlit
    col1, col2 = st.columns(2)
    with col1:
        st.title("Ouro Mensal")
        st.plotly_chart(fig4, use_container_width=True)
    with col2:
        st.title("Insumos Mensal")
        st.plotly_chart(fig2, use_container_width=True)


    ###############################################################
    ######### Cria Tabela #################################

    col1, col2 = st.columns(2)
    with col1:
        #st.title("Ouro Mensal")
        st.dataframe(df_Etiqueta_geral[['ano_pedido', 'mes_pedido', 'ped_peso_corr', 'fab_peso_corr', 'acum_peso_corr']])
    with col2:
        #st.title("Insumos Mensal")
        st.dataframe(df_Etiqueta_geral[['ano_pedido', 'mes_pedido', 'insumo_ped','insumo_fab', 'acum_insumos_aberto']])


    st.title("ANALISE EM R$")
    col1, col2 = st.columns(2)
    with col1:
        #st.title("Pedido")
        st.dataframe(df_Etiqueta_geral[['ano_pedido', 'mes_pedido', 'ped_valor_metal_corr', 'ped_valor_out_corr', 'ped_valor_pedras_corr','ped_valor_servicos_corr']])
    with col2:
        #st.title("Fabricado")
        st.dataframe(df_Etiqueta_geral[['ano_pedido', 'mes_pedido', 'fab_valor_metal_corr', 'fab_valor_out_corr', 'fab_valor_pedras_corr','fab_valor_servicos_corr']])



    print(df_Etiqueta_geral.head())
    print(df_Etiqueta_geral.dtypes)

        ###########################################################
        ###########################################################

