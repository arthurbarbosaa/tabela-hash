import requests
from tabela_hash import HashTable
import time

def buscar_no_cache(cache, entrada):
    start_time = time.time()
    resultado = cache.search(entrada.lower())
    if resultado is not None:
        print("[CACHE] Resultado encontrado no cache:")
        print(f"Tempo de execução: {time.time() - start_time:.4f} segundos")
        return resultado, True
    print(f"Tempo de execução: {time.time() - start_time:.4f} segundos")
    return None, False

def consultar_api(entrada):
    start_time = time.time()
    url = f"https://restcountries.com/v3.1/name/{entrada}"
    try:
        resposta = requests.get(url, timeout=5)
        resposta.raise_for_status()
        dados = resposta.json()
        if isinstance(dados, list) and len(dados) > 0:
            pais = dados[0]
            nome = pais.get('name', {}).get('common', 'N/A')
            capital = pais.get('capital', ['N/A'])[0]
            populacao = pais.get('population', 'N/A')
            print(f"Tempo de execução: {time.time() - start_time:.4f} segundos")
            return {'nome': nome, 'capital': capital, 'populacao': populacao}
        else:
            print("[ERRO] País não encontrado na API.")
            print(f"Tempo de execução: {time.time() - start_time:.4f} segundos")
            return None
    except requests.exceptions.RequestException as e:
        print(f"[ERRO] Erro de rede ou requisição: {e}")
        print(f"Tempo de execução: {time.time() - start_time:.4f} segundos")
        return None
    except Exception as e:
        print(f"[ERRO] Erro inesperado: {e}")
        print(f"Tempo de execução: {time.time() - start_time:.4f} segundos")
        return None

def main():
    cache = HashTable()
    while True:
        entrada = input("Digite o nome de um país (ou 'sair' para encerrar): ").strip()
        if entrada.lower() == 'sair':
            print("Encerrando o programa.")
            break
        if not entrada:
            print("[ERRO] Entrada vazia. Tente novamente.")
            continue
        resultado, veio_do_cache = buscar_no_cache(cache, entrada)
        if resultado:
            print(f"Nome: {resultado['nome']}")
            print(f"Capital: {resultado['capital']}")
            print(f"População: {resultado['populacao']}")
            print("---")
            continue
        resultado = consultar_api(entrada)
        if resultado:
            cache.insert(entrada.lower(), resultado)
            print("[API] Resultado obtido da API:")
            print(f"Nome: {resultado['nome']}")
            print(f"Capital: {resultado['capital']}")
            print(f"População: {resultado['populacao']}")
            print("---")
        else:
            print("[ERRO] Não foi possível obter informações para essa entrada.")

if __name__ == "__main__":
    main()