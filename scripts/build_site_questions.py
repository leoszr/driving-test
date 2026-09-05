import os
import re
import json

# Load the audited site bank and the newly extracted datasets.
with open("archive/questions.json", "r", encoding="utf-8") as f:
    archived = json.load(f)

with open("extracted_data/epermit_final.json", "r", encoding="utf-8") as f:
    epermit = json.load(f)

with open("extracted_data/dontredriving_final.json", "r", encoding="utf-8") as f:
    dont = json.load(f)


site_questions = []
seen_questions = set()

def normalize_text(text):
    text = re.sub(r"[^a-záéíóúâêîôûãõç0-9\s]", "", text.lower())
    return " ".join(text.split())

def clean_text(text):
    return re.sub(r"\s+(?:[0Oo]\)|Dt)$", "", text.strip()).strip()

DANGLING_OPTION = re.compile(r"(?:[,;:]|\b(?:a|à|ao|aos|de|do|da|dos|das|e|ou|que|para|com|em|no|na|seu|sua|uma|um))$", re.IGNORECASE)

def valid_extracted_options(options):
    cleaned = [clean_text(option) for option in options]
    return (
        len(cleaned) == 4
        and len({normalize_text(option) for option in cleaned}) == 4
        and all(not DANGLING_OPTION.search(option) for option in cleaned)
    )


def add_question(question, options, answer, image=None):
    question = clean_text(question)
    options = [clean_text(option) for option in options]
    if not question or len(options) < 2 or not 0 <= answer < len(options):
        raise ValueError(f"Invalid question: {question!r}")

    key = f"{normalize_text(question)}___{normalize_text(options[0])}"
    if key in seen_questions:
        return False

    item = {"question": question, "options": options, "answer": answer}
    if image:
        item["image"] = image
    site_questions.append(item)
    seen_questions.add(key)
    return True

for q in archived:
    add_question(q["question"], q["options"], q["answer"], q.get("image"))

archived_count = len(site_questions)


# ePermitTest questions: Portuguese text, verified answers and illustrations.
for q in epermit:
    option_keys = sorted(q["options"])
    options = [q["options"][key] for key in option_keys]
    add_question(q["question"], options, option_keys.index(q["answer"]), q.get("image"))


# dontredriving questions: include only answers explicitly identified in the prints.
for q in dont:
    answer_key = q.get("gabarito")
    option_keys = sorted(q.get("options", {}))
    if answer_key in option_keys:
        options = [q["options"][key] for key in option_keys]
        if valid_extracted_options(options):
            add_question(q["question"], options, option_keys.index(answer_key))


# 3. Selected DMV Written Test questions with translations and verified answers
# High-yield NJ MVC questions translated accurately to Brazilian Portuguese
dmv_translations = {
    "DMV-01": {
        "question": "Motoristas com menos de 21 anos que operam com uma carteira probatória (Probationary License) devem exibir em sua placa:",
        "options": ["Um decalque vermelho", "Dois decalques refletivos vermelhos (GDL)", "Um adesivo amarelo", "Nenhum decalque"],
        "answer": 1,
        "explanation": "De acordo com a Kyleigh's Law de New Jersey, motoristas com permissão GDL ou carteira probatória com menos de 21 anos devem afixar dois decalques refletivos vermelhos em cada placa."
    },
    "DMV-02": {
        "question": "Durante o período probatório após receber uma permissão especial de aprendiz, o motorista não pode acumular mais de quantos pontos antes de ser matriculado no Programa de Motorista Probatório?",
        "options": ["4 pontos (ou duas infrações)", "2 pontos", "6 pontos", "8 pontos"],
        "answer": 0,
        "explanation": "Um motorista probatório é obrigado a se matricular no Programa de Motorista Probatório se acumular 4 ou mais pontos ou for condenado por duas ou mais infrações de trânsito."
    },
    "DMV-03": {
        "question": "Após a restituição de uma carteira de motorista suspensa, o motorista estará em período probatório de direção por:",
        "options": ["6 meses", "Um ano", "Dois anos", "9 meses"],
        "answer": 1,
        "explanation": "Após a restauração dos privilégios de direção suspensos, o motorista passa por um período probatório de um ano."
    },
    "DMV-06": {
        "question": "Esta placa de regulamentação significa:",
        "options": ["Fim de rodovia dividida", "Trânsito em sentido único à frente", "Trânsito em sentido duplo à frente", "Mantenha-se à direita (Keep Right)"],
        "answer": 3,
        "image": "images/i606.png",
        "explanation": "Esta placa regulamentar indica que os motoristas devem manter seus veículos à direita de uma barreira, ilha de tráfego ou divisor de pista."
    },
    "DMV-07": {
        "question": "Qual é a primeira coisa que você deve ajustar, se necessário, ao entrar no carro para dirigir?",
        "options": ["O espelho retrovisor interno", "Os espelhos laterais externos", "O volante", "O seu assento (banco)"],
        "answer": 3,
        "explanation": "Antes de ajustar espelhos ou outros comandos, você deve ajustar o assento para que alcance confortavelmente os pedais e controle o volante."
    },
    "DMV-08": {
        "question": "Você está dirigindo em uma via movimentada e o acelerador do veículo fica preso (travado). Você deve:",
        "options": ["Pisar no freio com toda força sem desligar", "Puxar o freio de mão imediatamente", "Mudar para neutro (ponto morto) e frear com segurança", "Desligar a ignição travando o volante"],
        "answer": 2,
        "explanation": "Se o acelerador travar, mude imediatamente para o ponto morto (neutro), aplique os freios e conduza o veículo com segurança para fora da pista."
    },
    "DMV-09": {
        "question": "Você está aguardando no cruzamento para completar uma conversão à esquerda. Você deve:",
        "options": ["Manter as rodas viradas para a esquerda", "Avançar lentamente mesmo sem visão", "Sinalizar e manter as rodas retas até poder virar", "Buzinar para o tráfego que se aproxima"],
        "answer": 2,
        "explanation": "Ao aguardar para virar à esquerda, mantenha as rodas retas. Se outro veículo colidir na traseira do seu carro, você não será projetado contra o tráfego contrário."
    },
    "DMV-10": {
        "question": "Esta placa de trânsito adverte:",
        "options": ["Atenção a ciclistas / Bicicletas na via", "Bicicletas proibidas", "Oficina de bicicletas à frente", "Ciclistas têm preferência obrigatória"],
        "answer": 0,
        "image": "images/i607.png",
        "explanation": "Esta placa de advertência avisa que bicicletas podem estar cruzando ou compartilhando a via naquela área."
    },
    "DMV-11": {
        "question": "Qual dos seguintes NÃO é um fator que determina a distância necessária para parar o veículo?",
        "options": ["A capacidade de esterçamento do volante", "Tempo de reação do motorista", "Condição dos freios e pneus", "Condições climáticas e visibilidade"],
        "answer": 0,
        "explanation": "A distância de parada é composta pela distância de reação e distância de frenagem. A capacidade do volante não diminui o tempo/distância de parada."
    },
    "DMV-12": {
        "question": "Se os limpadores de para-brisa falharem repentinamente durante chuva ou neve, você deve:",
        "options": ["Ligar as luzes de emergência (pisca-alerta)", "Desacelerar e encostar fora da pista de rolamento", "Abrir a janela para manter a visão se necessário", "Todas as alternativas acima"],
        "answer": 3,
        "explanation": "Em caso de falha nos limpadores com baixa visibilidade, reduza a velocidade, acione o pisca-alerta e saia da estrada com segurança."
    },
    "DMV-14": {
        "question": "Esta seta verde em um sinal de controle de faixa indica que:",
        "options": ["Você pode utilizar esta faixa", "O trânsito é proibido nesta faixa", "Você tem preferência absoluta", "Você deve mudar de faixa imediatamente"],
        "answer": 0,
        "image": "images/i608.png",
        "explanation": "Um sinal de seta verde apontando para baixo significa que a faixa correspondente está aberta para circulação de tráfego."
    },
    "DMV-16": {
        "question": "Um motorista com 21 anos ou mais que esteja operando com permissão GDL deve praticar direção supervisionada por pelo menos quanto tempo antes do exame prático?",
        "options": ["6 meses", "3 meses", "1 mês", "2 semanas"],
        "answer": 1,
        "explanation": "Candidatos ao exame de direção com 21 anos ou mais no sistema GDL de New Jersey são obrigados a praticar por pelo menos 3 meses supervisionados."
    },
    "DMV-17": {
        "question": "Se você precisar parar rapidamente e seu veículo NÃO for equipado com Sistema de Freios Antibloqueio (ABS), você deve:",
        "options": ["Segurar o pedal do freio até o fundo continuamente", "Bombear os freios com firmeza", "Tocar os freios levemente", "Soltar o pedal do freio e usar apenas a embreagem"],
        "answer": 1,
        "explanation": "Em veículos convencionais sem ABS, bombear os freios com firmeza evita o travamento das rodas e permite que o motorista continue mantendo o controle da direção."
    },
    "DMV-18": {
        "question": "O que é uma 'No Zone' (Zona Sem Visão) de acordo com o manual do NJ MVC?",
        "options": ["Uma área onde é proibido estacionar", "Uma via exclusiva de pedestres", "Os grandes pontos cegos ao redor de caminhões e veículos de grande porte", "Uma zona de silêncio próximo a hospitais"],
        "answer": 2,
        "explanation": "'No Zones' são os pontos cegos dianteiro, traseiro e laterais dos caminhões. Se você não puder ver o motorista nos espelhos dele, ele não pode ver você."
    },
    "DMV-19": {
        "question": "A maneira correta de utilizar uma rampa de desaceleração (saída de rodovia expressa) é:",
        "options": ["Reduzir a velocidade antes de entrar na rampa de saída", "Reduzir a velocidade somente após entrar na rampa de saída", "Manter a velocidade máxima até o final da rampa", "Ultrapassar veículos mais lentos na rampa"],
        "answer": 1,
        "explanation": "Não diminua a velocidade na pista principal da rodovia; entre na rampa de desaceleração na velocidade de fluxo e reduza dentro da rampa."
    },
    "DMV-20": {
        "question": "Parar completamente em um cruzamento, ceder a preferência a pedestres e tráfego transversal, e depois prosseguir quando estiver livre corresponde a qual sinal?",
        "options": ["Luz amarela piscante", "Luz verde constante", "Luz amarela contínua", "Luz vermelha piscante"],
        "answer": 3,
        "explanation": "Uma luz vermelha piscante tem o mesmo significado legal de uma placa de parada obrigatória (STOP)."
    },
    "DMV-21": {
        "question": "Ao estacionar em subida (aclive) em uma rua com meio-fio (guia):",
        "options": ["Vire as rodas em direção ao meio-fio", "Vire as rodas para o lado oposto ao meio-fio (para fora da guia)", "Mantenha as rodas estritamente retas", "Vire as rodas ligeiramente para a direita"],
        "answer": 1,
        "explanation": "Em aclive com guia, as rodas dianteiras devem ser viradas na direção oposta ao meio-fio (para a esquerda), para que a traseira dos pneus apoie na guia caso o carro se mova."
    },
    "DMV-23": {
        "question": "Qual das seguintes luzes de semáforo indica que você deve diminuir a velocidade e prosseguir com cautela em um cruzamento?",
        "options": ["Luz amarela piscante", "Luz vermelha piscante", "Luz verde intermitente", "Luz amarela contínua"],
        "answer": 0,
        "explanation": "Luz amarela piscante alerta os motoristas para reduzir a velocidade e atravessar a interseção com atenção redobrada."
    },
    "DMV-24": {
        "question": "A aquaplanagem (hidroplanagem) é normalmente causada por:",
        "options": ["Pneus com calibragem excessiva", "Pistas recém-pavimentadas e secas", "Combinação de velocidade alta com pneus gastos ou lâmina d'água na pista", "Uso indevido do freio de mão"],
        "answer": 2,
        "explanation": "A hidroplanagem ocorre quando os pneus perdem contato com a superfície da estrada devido ao acúmulo de água sob a banda de rodagem em alta velocidade."
    },
    "DMV-25": {
        "question": "Em uma via que não possui calçadas para pedestres, o pedestre deve caminhar:",
        "options": ["Do mesmo lado em que o tráfego está se movendo", "De frente para o tráfego que se aproxima (lado esquerdo da via)", "No centro da via para ser visto", "Onde for mais conveniente"],
        "answer": 1,
        "explanation": "Quando não houver calçada, os pedestres devem sempre caminhar no acostamento de frente para o tráfego que se aproxima."
    },
    "DMV-26": {
        "question": "Ao entrar em uma via pública saindo de uma garagem ou via de acesso privada, você:",
        "options": ["Tem preferência sobre o trânsito da rua", "Deve buzinar e avançar rapidamente", "Deve parar totalmente e ceder a preferência a pedestres e veículos", "Pode ingressar se a pista estiver 50% livre"],
        "answer": 2,
        "explanation": "Veículos saindo de garagens, becos ou propriedades privadas devem parar e conceder a preferência a todos os veículos e pedestres."
    },
    "DMV-27": {
        "question": "Beber café após consumir bebidas alcoólicas:",
        "options": ["Reduz rapidamente a taxa de álcool no sangue (BAC)", "Não tem nenhum efeito sobre a taxa de álcool no sangue (BAC)", "Ajuda a recuperar os reflexos e a coordenação motora", "Acelera a eliminação do álcool pelo fígado"],
        "answer": 1,
        "explanation": "Apenas o tempo pode deixar uma pessoa sóbria. Café, banhos frios ou exercícios não reduzem a concentração de álcool no sangue."
    },
    "DMV-28": {
        "question": "Placas de trânsito em formato de triângulo invertido (apontando para baixo) instruem os motoristas a:",
        "options": ["Parar obrigatoriamente", "Ceder a preferência (Yield)", "Aumentar a velocidade", "Atenção a obras na via"],
        "answer": 1,
        "explanation": "O triângulo invertido de três lados é o formato universal e exclusivo das placas de 'Dê a Preferência' (Yield)."
    },
    "DMV-29": {
        "question": "Placas de trânsito no formato de flâmula (triângulo deitado) indicam:",
        "options": ["Zonas de pedestres", "Zonas onde é proibido ultrapassar (No Passing Zone)", "Fim de rodovia", "Entrada em rotatória"],
        "answer": 1,
        "explanation": "Uma placa em formato de flâmula (pennant) é posicionada no lado esquerdo da via indicando o início de uma zona de não ultrapassagem."
    },
    "DMV-30": {
        "question": "Quando é ilegal dirigir abaixo do limite de velocidade regulamentado?",
        "options": ["Quando a velocidade excessivamente lenta atrapalha ou bloqueia o fluxo normal do tráfego", "Durante condições de chuva pesada", "Ao rebocar um reboque", "Nunca é proibido"],
        "answer": 0,
        "explanation": "É contra a lei dirigir tão devagar que bloqueie ou impeça o fluxo normal e razoável do tráfego, exceto quando necessário para a segurança."
    },
    "DMV-31": {
        "question": "As placas de regulamentação (Regulatory Signs) geralmente possuem fundo de qual cor?",
        "options": ["Branco", "Amarelo", "Azul", "Laranja"],
        "answer": 0,
        "explanation": "Placas regulamentares (como limites de velocidade e regras de trânsito) são tipicamente retangulares brancas com letras e números pretos."
    },
    "DMV-32": {
        "question": "Esta placa de advertência avisa que:",
        "options": ["Você deve virar obrigatoriamente", "Você está se aproximando do início de uma rodovia dividida por canteiro central", "A rodovia dividida termina à frente", "Há um cruzamento em nível de quatro vias"],
        "answer": 1,
        "image": "images/i609.png",
        "explanation": "Esta placa (Divided Highway Ahead) avisa que a pista à frente será dividida por uma barreira central ou canteiro."
    },
    "DMV-34": {
        "question": "O braço e a mão esquerdos do motorista estão estendidos para fora da janela dobrados para cima em 90 graus. Este sinal manual significa que o motorista pretende:",
        "options": ["Virar à esquerda", "Virar à direita", "Parar ou diminuir a marcha", "Seguir em frente"],
        "answer": 1,
        "image": "images/i610.png",
        "explanation": "O braço esquerdo para fora dobrado em ângulo reto apontando para cima sinaliza a intenção de conversão à direita."
    },
    "DMV-39": {
        "question": "Em New Jersey, os veículos a motor não devem ficar funcionando em marcha lenta (idling) desnecessariamente por mais de:",
        "options": ["3 minutos", "5 minutos", "10 minutos", "15 minutos"],
        "answer": 0,
        "explanation": "A lei de New Jersey proíbe que veículos fiquem funcionando em marcha lenta desnecessária por mais de 3 minutos consecutivos."
    },
    "DMV-43": {
        "question": "Ao dirigir em condições de neblina espessa, você deve utilizar:",
        "options": ["Faróis altos (luz alta)", "Faróis baixos (luz baixa)", "Apenas as luzes de estacionamento", "Apenas o pisca-alerta"],
        "answer": 1,
        "explanation": "A luz alta reflete nas gotículas de água da neblina de volta para os olhos do motorista. Sempre use os faróis baixos."
    },
    "DMV-44": {
        "question": "Para verificar seu ponto cego ao mudar de faixa para a esquerda, você deve:",
        "options": ["Olhar apenas pelo retrovisor interno", "Olhar apenas pelo espelho retrovisor esquerdo", "Olhar rapidamente por cima do seu ombro esquerdo", "Buzinar antes de esterçar o volante"],
        "answer": 2,
        "explanation": "Espelhos retrovisores não cobrem todos os ângulos; um rápido olhar sobre o ombro correspondente é essencial antes de mudar de faixa."
    },
    "DMV-61": {
        "question": "O que significa uma linha branca simples e tracejada separando as faixas de tráfego?",
        "options": ["O tráfego flui em direções opostas e a ultrapassagem é proibida", "A mudança de faixa é terminantemente proibida", "A via é exclusiva para ônibus", "As faixas fluem no mesmo sentido e a ultrapassagem é permitida quando segura"],
        "answer": 3,
        "explanation": "Linhas brancas separam faixas no mesmo sentido; linhas tracejadas indicam que a mudança de faixa e ultrapassagem são permitidas com segurança."
    },
    "DMV-62": {
        "question": "Quais são as cores das placas de sinalização que informam saídas e destinos em rodovias?",
        "options": ["Azul com letras brancas", "Marrom com letras amarelas", "Branca com letras pretas", "Verde com letras brancas"],
        "answer": 3,
        "explanation": "Placas de orientação de destinos e saídas em autoestradas possuem fundo verde com inscrições em branco."
    },
    "DMV-66": {
        "question": "Ao realizar uma conversão à esquerda em uma via de mão dupla, você NÃO deve:",
        "options": ["Sinalizar com antecedência de 100 pés", "Cortar a quina (curva fechada demais entrando na pista contrária)", "Ceder a preferência ao tráfego em sentido contrário", "Manter as rodas retas enquanto aguarda"],
        "answer": 1,
        "explanation": "Cortar os cantos em conversões à esquerda é perigoso porque coloca seu veículo na trajetória dos carros que circulam na via transversal."
    },
    "DMV-69": {
        "question": "Você se aproxima de um cruzamento com uma luz vermelha piscante no semáforo. Você deve:",
        "options": ["Reduzir a velocidade e cruzar sem parar se não houver tráfego", "Aumentar a velocidade para liberar o cruzamento", "Parar completamente e prosseguir somente quando a pista estiver desimpedida", "Aguardar a luz ficar verde contínua"],
        "answer": 2,
        "explanation": "Trate uma luz vermelha piscante exatamente como uma placa de pare (STOP sign)."
    },
    "DMV-79": {
        "question": "Em uma rodovia de pistas múltiplas, o tráfego que se desloca em velocidade mais lenta deve:",
        "options": ["Trafegar na faixa da extrema esquerda", "Trafegar na faixa central", "Trafegar pelo acostamento", "Manter-se na faixa da extrema direita"],
        "answer": 3,
        "explanation": "A lei de New Jersey exige que o motorista se mantenha à direita, exceto para ultrapassar outros veículos."
    },
    "DMV-81": {
        "question": "Você pode cruzar uma linha amarela dupla contínua no centro da pista:",
        "options": ["Para ultrapassar veículos lentos", "Para realizar uma conversão entrando em uma entrada de garagem particular ou rua", "Apenas durante a noite", "Sob nenhuma circunstância"],
        "answer": 1,
        "explanation": "Linhas amarelas contínuas proíbem a ultrapassagem, mas você pode cruzá-las para entrar ou sair de garagens ou entradas privadas."
    },
    "DMV-91": {
        "question": "Ao visualizar esta placa de regulamentação ('DO NOT PASS'), você:",
        "options": ["Não deve ultrapassar outro veículo naquela área", "Pode ultrapassar veículos que estejam a menos de 20 mph", "Pode ultrapassar se conhecer bem a estrada", "Pode ultrapassar apenas no período noturno"],
        "answer": 0,
        "image": "images/i613.png",
        "explanation": "A placa 'DO NOT PASS' marca o início de um trecho onde toda ultrapassagem de veículos motorizados é proibida por lei."
    }
}

for data in dmv_translations.values():
    add_question(
        data["question"],
        data["options"],
        data["answer"],
        data.get("image"),
    )


# Fail the build rather than ship malformed data or broken image links.
banned_ocr = re.compile(r"Fourgreenstickers|T———|POR NE|FE CEI|TES IE|(?:^|\s)[0Oo]\)(?:\s|$)|\bDt$")
for q in site_questions:
    assert not banned_ocr.search(" ".join([q["question"], *q["options"]])), q
    if q.get("image"):
        assert os.path.isfile(q["image"]), q["image"]

with open("questions.json", "w", encoding="utf-8") as f:
    json.dump(site_questions, f, indent=2, ensure_ascii=False)

print(f"Existing bank: {archived_count}")
print(f"New unique questions: {len(site_questions) - archived_count}")
print(f"Published bank: {len(site_questions)}")
