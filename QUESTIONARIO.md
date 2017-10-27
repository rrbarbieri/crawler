# Questionário

* **Agora você tem de capturar dados de outros 100 sites. Quais seriam suas estratégias para escalar a aplicação?**

A solução proposta para esse desafio já leva em consideração a escalabilidade, já que é uma solução me arquitetura distribuída que utiliza a framework dispy (http://dispy.sourceforge.net/index.html). O aplicativo pode ser executado tanto em modo autônomo, em um único computador, ou em um cluster, em um sistema distribuído por vários computadores dentro de uma rede. No modo de cluster, como o aplicativo faz uso de banco de dados MySQL para armazenar as informações coletadas dos sites visitados, essas informações estão disponíveis para serem processadas por qualquer job sendo executado nos nós do cluster. Além disso, em caso de interrupção, o processamento pode ser retomado a qualquer momento sem perda de dados. O URL do site a visitar pode ser passado como um argumento ou como uma opção da linha de comando com o nome do arquivo contendo uma lista de sites a serem visitados.

Os links que foram seguidos em cada uma das páginas visitadas são armazenados como entradas distintas em uma tabela de banco de dados para que esses links não sejam revisitados. Os links armazenados podem ser processados ​​em paralelo por qualquer job no cluster. Uma vez selecionado, um link não estará disponível para os outros jobs do cluster, embora o job de processamento possa rastrear e armazenar novos links da página visitada e esses links, por conseguinte, estarão disponíveis para outros jobs do cluster. Se a página visitada corresponder a um produto sendo vendido, suas informações serão armazenadas em outra tabela de banco de dados. Um link será considerado visitado quando todas as informações coletadas da página visitada forem coletadas e armazenadas com sucesso, incluindo as de um eventual produto vendido. Os jobs do aplicativo rodando no cluster terminam a execução quando não há mais links para visitar.

Um arquivo .csv com uma lista dos produtos encontrados pode ser gerado no final.

* Alguns sites carregam o preço através de JavaScript. Como faria para capturar esse valor.

Uma forma de extrair dados de páginas cuja parte do conteúdo seja gerada por código JavaScript, o qual é executado no navegador, é
obter o array JavaScript contido no elemento da página e convertê-lo para XML utilizando js2xml. Outra forma é terceirizar a tarefa de renderizar a página completa para um navegador web. Assim, ao invés de utilizar o HTML baixado, uma ferramenta tal como PhantomJS pode fazer com que um navegador baixe a página e execute o código JS, e então entregue como resposta o HTML pronto. PhantomJS é um navegador headless que pode ser facilmente integrado com Python via Selenium.

* Alguns sites podem bloquear a captura por interpretar seus acessos como um ataque DDOS. Como lidaria com essa situação?

A solução proposta, por ser em arquitetura distribuída, permite a execução de instâncias independentes do aplicativo (jobs) em máquinas que fazem parte do cluster mas que podem estar em outras redes. Assim, de certa forma, é possível burlar a proteção anti-DDoS já que as diversas requisições são enviadas simultaneamente a partir de vários pontos diferentes da rede.

* Um cliente liga reclamando que está fazendo muitos acessos ao seu site e aumentando seus custos com infra. Como resolveria esse problema?

Na solução proposta é possível determinar a quantidade de jobs do aplicativo que serão executados nos nós do cluster e assim reduzir o número de requisições simultâneas em horários de maior intensidade de acessos, e aumentar a quantidade de jobs do aplicativo naqueles horários em que a intensidade de acesso não seja tão grande. Como o aplicativo pode ser interrompido sem que haja perda de dados, é possível retomar o processamento com uma quantidade diferente de jobs. Além disso, é possível determinar a profundidade máxima dos links que serão seguidos e assim reduzir a quantidade de trabalho a processar em cada execução.



