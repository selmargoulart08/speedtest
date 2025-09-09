Aplicativo de Teste de Velocidade de Internet
Descrição
Este é um aplicativo de desktop simples para Windows, Mac e Linux que mede a velocidade de download e upload da sua conexão com a internet. O aplicativo utiliza a biblioteca speedtest-cli para realizar os testes e a biblioteca tkinter para a interface gráfica.

Com este aplicativo, você pode:

Realizar testes de velocidade de forma fácil e rápida.

Acompanhar seu histórico de testes.

Visualizar o desempenho da sua conexão ao longo do tempo em um gráfico interativo.

Exportar os resultados do histórico para um arquivo CSV.

Obter informações detalhadas como ping, jitter e perda de pacotes.

Funcionalidades Principais
Interface Amigável: Design em modo escuro, com um medidor de progresso no formato de círculo para uma experiência visual agradável.

Histórico de Testes: Todos os testes realizados são salvos em um arquivo local (test_history.json) e exibidos em uma tabela na interface.

Gráfico de Desempenho: Um gráfico interativo mostra a evolução das velocidades de download e upload ao longo do tempo.

Exportação de Dados: Um botão dedicado permite exportar todo o histórico de testes para um arquivo CSV, ideal para análise em planilhas.

Métricas Avançadas: O aplicativo exibe métricas importantes para jogos e streaming, como Ping, Jitter e Perda de Pacotes.

Otimização de Servidor: O aplicativo seleciona automaticamente o melhor servidor para o teste, garantindo a maior precisão possível nos resultados.

Requisitos
Para rodar o aplicativo, você precisa ter o Python 3 instalado e as seguintes bibliotecas:

pip install tkinter
pip install speedtest-cli
pip install matplotlib

Como Usar
Clone ou baixe este repositório para o seu computador.

Abra o terminal ou prompt de comando na pasta onde o arquivo speed_test_app.py está.

Execute o script com o seguinte comando:

python speed_test_app.py

A janela do aplicativo irá abrir. Pressione o botão "Iniciar Teste" para começar a medição.

Contribuição
Contribuições são bem-vindas! Se você tiver alguma ideia para melhorar o aplicativo ou encontrar algum bug, sinta-se à vontade para abrir uma issue ou enviar um pull request.

Futuras Melhorias
Adicionar um botão para exportar o gráfico como imagem.

Incluir a opção de um teste contínuo para monitorar a conexão em tempo real.

Criar um aplicativo executável para Windows, Mac e Linux, eliminando a necessidade de instalar o Python e as bibliotecas.
