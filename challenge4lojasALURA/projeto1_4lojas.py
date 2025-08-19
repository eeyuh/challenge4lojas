import pandas as pd
import matplotlib.pyplot as plt

# Ler arquivos CSV 
loja1 = pd.read_csv("loja_1.csv")
loja2 = pd.read_csv("loja_2.csv")
loja3 = pd.read_csv("loja_3.csv")
loja4 = pd.read_csv("loja_4.csv")

# Criar colunas para identificar cada loja 
loja1["Loja"] = "Loja 1"
loja2["Loja"] = "Loja 2"
loja3["Loja"] = "Loja 3"
loja4["Loja"] = "Loja 4"

# Juntar tudo em uma tabela 
dados = pd.concat([loja1, loja2, loja3, loja4], ignore_index=True)

# Tratar nomes de colunas e tipos de dados
dados.columns = dados.columns.str.strip()  # remove espaços extras
dados["Preço"] = pd.to_numeric(dados["Preço"], errors='coerce')
dados["Quantidade de parcelas"] = pd.to_numeric(dados["Quantidade de parcelas"], errors='coerce')
dados["Frete"] = pd.to_numeric(dados["Frete"], errors='coerce')
dados["Avaliação da compra"] = pd.to_numeric(dados["Avaliação da compra"], errors='coerce')

# Criar coluna de faturamento 
dados["Faturamento"] = dados["Preço"] * dados["Quantidade de parcelas"]

# Faturamento total por loja
faturamento_loja = dados.groupby('Loja')['Faturamento'].sum()
print("Faturamento total por loja:\n", faturamento_loja, "\n")

# Categorias mais populares por loja 
categorias_populares = dados.groupby(['Loja', 'Categoria do Produto'])['Quantidade de parcelas'].sum()
categorias_populares = categorias_populares.groupby('Loja', group_keys=False).nlargest(1)
print("Categoria mais popular por loja:\n", categorias_populares, "\n")

# Média de avaliação dos clientes por loja 
avaliacao_media = dados.groupby('Loja')['Avaliação da compra'].mean()
print("Média de avaliação dos clientes:\n", avaliacao_media, "\n")

# Produtos mais e menos vendidos por loja 
produtos_vendidos = dados.groupby(['Loja', 'Produto'])['Quantidade de parcelas'].sum()
mais_vendido = produtos_vendidos.groupby('Loja').idxmax()
menos_vendido = produtos_vendidos.groupby('Loja').idxmin()
print("Produtos mais vendidos por loja:\n", mais_vendido, "\n")
print("Produtos menos vendidos por loja:\n", menos_vendido, "\n")

# Custo médio do frete por loja
frete_medio = dados.groupby('Loja')['Frete'].mean()
print("Custo médio do frete por loja:\n", frete_medio, "\n")

# Rendimento = Faturamento total - Frete médio
rendimento = faturamento_loja - frete_medio
loja_menor_rendimento = rendimento.idxmin()
print("Loja com menor rendimento:", loja_menor_rendimento, "\n")

# ===== GRÁFICOS (apenas no final) =====

#Gráfico de barras: Faturamento total por loja
plt.figure(figsize=(8,5))
plt.bar(faturamento_loja.index, faturamento_loja.values, color='skyblue')
plt.title("Faturamento Total por Loja")
plt.xlabel("Loja")
plt.ylabel("Faturamento (R$)")
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

#Gráfico de pizza: Distribuição das categorias de produtos
categorias_totais = dados.groupby('Categoria do Produto')['Quantidade de parcelas'].sum()
plt.figure(figsize=(8,8))
plt.pie(categorias_totais.values, labels=categorias_totais.index, autopct='%1.1f%%', startangle=140, colors=plt.cm.tab20.colors)
plt.title("Distribuição das Categorias de Produtos")
plt.show()

#Gráfico de dispersão: Avaliação média vs. Custo médio do frete
avaliacao_frete = dados.groupby('Loja').agg({'Avaliação da compra':'mean', 'Frete':'mean'})
plt.figure(figsize=(8,5))
plt.scatter(avaliacao_frete['Frete'], avaliacao_frete['Avaliação da compra'], color='orange', s=100)
for i, txt in enumerate(avaliacao_frete.index):
    plt.annotate(txt, (avaliacao_frete['Frete'][i]+0.1, avaliacao_frete['Avaliação da compra'][i]+0.01))
plt.title("Avaliação Média vs. Custo Médio do Frete")
plt.xlabel("Frete Médio (R$)")
plt.ylabel("Avaliação Média")
plt.grid(True, linestyle='--', alpha=0.7)
plt.show()

#===EXTRA===#
# Garantir que lat e lon sejam numéricos
dados["lat"] = pd.to_numeric(dados["lat"], errors='coerce')
dados["lon"] = pd.to_numeric(dados["lon"], errors='coerce')

# Criar gráfico de dispersão geográfico: localização das vendas
plt.figure(figsize=(10,7))
# O tamanho do ponto pode refletir o faturamento de cada compra
plt.scatter(dados['lon'], dados['lat'], s=dados['Faturamento']/10,  # ajusta tamanho para visualização
            c=dados['Faturamento'], cmap='viridis', alpha=0.6, edgecolors='w')

plt.colorbar(label='Faturamento (R$)')
plt.title("Distribuição Geográfica das Vendas")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.grid(True, linestyle='--', alpha=0.5)
plt.show()


