import pandas as pd
from openai import OpenAI

def load_data(file_path):
    """엑셀 파일을 읽어 DataFrame으로 반환하는 함수"""
    data = pd.read_excel(file_path)
    print("데이터 로드 완료!")
    print(data.head())
    return data

def process_with_openai(data, base_url):
    """OpenAI 클라이언트를 사용해 요청을 처리하는 함수"""
    results = []

    for index, row in data.iterrows():
        # 기존 add_feature 함수 사용하여 메시지 구조 생성
        message_structure = add_feature(row["id"], row["question"])

        # OpenAI 클라이언트 설정
        client = OpenAI(
            base_url=base_url,
            api_key="dummy-key",
            default_headers={
                "Content-Type": "application/json",
                "Question-ID": str(row["id"])
            }
        )

        try:
            response = client.chat.completions.create(
                model="olympiad",
                messages=message_structure["message"],
                temperature=0.7,
                max_tokens=None,
                stream=False
            )

            # response를 dictionary로 변환
            response_dict = response.model_dump()
            result = response_dict.get('result', {})

            print(f"\nID {row['id']} 처리 완료")
            print(f"응답: {result.get('response', '')}")

            results.append({
                'id': row['id'],
                'question': row['question'],
                'prompt': result.get('prompt', ''),
                'context': result.get('context', ''),
                'response': result.get('response', ''),
                'score': result.get('score', 0),
                'reasoning': result.get('reasoning', '')
            })

        except Exception as e:
            print(f"ID {row['id']} 처리 중 에러 발생: {str(e)}")


    # 결과를 DataFrame으로 변환하고 엑셀로 저장
    results_df = pd.DataFrame(results)
    results_df.to_excel('response_results.xlsx', index=False)

def add_feature(id, question):
    """
    메시지 구조를 생성하는 함수
    - 이 함수는 학생들이 필요에 따라 시스템 메시지나 사용자 메시지를 추가로 정의하도록 설계되었습니다.
    - 아래의 system_prompt와 user_message를 수정하여 커스터마이즈하세요.

    :param id: int/str, ID
    :param question: str, 질문
    :return: dict, 메시지 JSON 구조
    """
    # -----------------수정--------------------#
    system_prompt = """
        너는 고도화된 LLM 전문가 봇이야.  
        다음 원칙을 반드시 지켜서, **오직 한국어로만** 답변해줘.  

        1. **정확도**를 최우선으로 하되, 정보가 불충분하면 무리해서 추측하지 말고 “추가 정보가 필요함” 등을 밝혀줘.  
        2. 질문의 의도를 **명확히 이해**한 뒤, 논리적인 사고 과정을 거쳐 가장 **타당하고 신뢰할 수 있는 답변**을 제시해줘.  
        3. **중요한 개념**이나 **핵심 아이디어**는 다른 사람이 이해하기 쉽도록 **간결하고 구체적인 한국어** 표현으로 설명해줘.  
        4. 필요한 경우, 문제 해결 과정을 **단계별**로 서술하거나, 근거가 되는 이론/자료를 **간단히 예시**로 들어서 답해줘.  
        5. 만약 질문이 애매하거나 추가 설명이 필요하다면, **추가 질문**을 통해 **정확한 맥락**을 파악해줘.  

        이러한 지침 아래에서, 사용자의 질문에 대해 **최대한 정확하고 명확**하게 답변하도록 해.  """  # 예: "이 모델은 질문 답변 시스템입니다."



    # -----------------수정--------------------#
    # 사용자 메시지 생성 (add_rag 함수에서 추가 처리)
    user_message = add_rag(question)

    # 메시지 구조 반환
    message = {
        "id": id,
        "message": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
    }
    return message


def add_rag(question):
    """
    질문에 추가 정보를 결합하는 함수
    - 이 함수는 학생들이 RAG(Retrieval-Augmented Generation)를 구현하거나, 질문에 추가 정보를 삽입하도록 설계되었습니다.
    - context를 활용해 질문에 정보를 추가하세요.

    :param question: str, 질문
    :return: str, 수정된 질문
    """
    # -----------------수정--------------------#
    context = """ 
        {
        "questions": [
            {"id": 1, "question": "인공지능(AI), 머신 러닝(ML), 딥 러닝(DL)의 차이를 간단히 설명하세요.", "context": ""},
            {"id": 2, "question": "Open AI의 GPT 모델에서 대해서 설명하시오", "context": "메타(구 페이스북)는 자사의 다양한 기술 및 제품에 LLaMA(Large Language Model Meta AI)를 활용하고 있습니다. LLaMA는 메타가 개발한 대형 언어 모델로, 자연어 처리(NLP)와 생성 AI 기술을 기반으로 하는 프로젝트에서 중요한 역할을 합니다. 구체적으로 메타는 다음과 같은 방식으로 LLaMA를 활용하고 있습니다.### 1. **리서치 및 개발**- **AI 연구**: LLaMA는 자연어 처리와 AI 언어 모델의 최첨단 기술 개발에 사용됩니다. 이를 통해 메타는 AI 연구 커뮤니티에 기여하고, NLP의 새로운 응용 가능성을 탐구합니다.- **효율적인 모델 구조**: LLaMA는 상대적으로 적은 자원으로도 고성능을 발휘하도록 설계되어, 메타의 AI 연구 효율성을 높이는 데 기여합니다.### 2. **사용자 경험 개선**- **챗봇 및 가상 비서**: 메타의 다양한 플랫폼(예: 메신저, WhatsApp)에서 LLaMA를 기반으로 한 자연어 처리 기술이 활용되어, 사용자와의 더 자연스러운 상호작용을 지원합니다.- **추천 시스템**: LLaMA는 콘텐츠 추천 및 검색 알고리즘을 강화하여, 사용자 맞춤형 피드와 광고를 더 정밀하게 제공합니다.### 3. **생성 AI 응용**- **콘텐츠 생성**: 메타의 플랫폼에서 사용자 생성 콘텐츠(UCG)를 지원하거나, 크리에이터를 위한 툴에 AI 기능을 추가하는 데 LLaMA가 사용됩니다.- **번역 및 다국어 지원**: 메타의 글로벌 사용자층을 위해 실시간 번역 및 다국어 상호작용 기술을 지원하는 데 사용됩니다.### 4. **오픈소스와 협력**- **AI 생태계 강화**: 메타는 LLaMA를 통해 AI 연구 커뮤니티와 협력하며, 모델과 데이터를 오픈소스화하여 연구자와 개발자들이 LLaMA를 활용할 수 있도록 지원합니다.### 5. **윤리적 AI 개발**- **안전하고 책임 있는 AI**: 메타는 LLaMA를 활용한 연구에서 AI의 편향성과 부정확성을 줄이고, 윤리적이고 공정한 모델을 개발하기 위한 노력을 지속하고 있습니다.LLaMA는 메타의 비즈니스 및 기술 생태계 전반에서 AI 기반의 효율성과 혁신을 촉진하는 핵심 도구로 자리 잡고 있습니다."},
            {"id": 3, "question": "메타는 라마를 어떻게 활용하고 있는가?", "context": ""},
            {"id": 4, "question": "가트너 그룹이 발표한 Hyper Cycle for Artificial Intelligence 2024에 대해서 설명하고 Computer Vision 기술은 어디쯤 위치해 있는지 설명하시오.", "context": ""},
            {"id": 5, "question": "1981년과 1995년 그리고 2009과 2023년에 대해서 각각 어떤 IT 이슈가 있었는지 설명하고 당시 성장한 주요 업체들을 나열하시오.", "context": ""},
            {"id": 6, "question": "Microsoft 가 OpenAI에 이제까지 투자하면서 얻은 것은 무엇인가?", "context": ""},
            {"id": 7, "question": "1990년대의 세계 최대의 부자들과 2020년의 최대 부자들을 비교하고 어떤 특이점이 있는지 기술하시오", "context": ""},
            {"id": 8, "question": "Microsoft의 사티아 CEO가 최근 Ignite 2024 행사에서 언급한 Scaling laws는 무엇인가?", "context": ""},
            {"id": 9, "question": "딥 러닝 모델의 파라메터 개수가 가지는 의미를 설명하시오", "context": ""},
            {"id": 10, "question": "제프리 힌튼 교수가 최근 노벨 상을 받았는데 어떤 분야이고 어떤 연구로 상을 받았는지 설명하시오", "context": ""},
            {"id": 11,"question": "LLM이 학습 과정에서 사용하는 '토큰화'의 의미는 무엇인가요?","context": "토큰화는 자연어 처리(NLP)에서 중요한 개념으로, 학습 과정에서 사용되는 주요 단어나 토큰을 분리하여 사용하는 과정입니다. 토큰화는 주로 다음과 같은 목적으로 사용됩니다: 1. **문서 전처리**: 텍스트 데이터를 단위로 나누어 분석하기 위해. 예를 들어, 단어, 문장, 문장의 주제 등이 토큰화되어 사용됩니다. 2. **데이터 크기 감소**: 텍스트 데이터의 크기를 줄여 학습 속도를 높이고, 데이터의 복잡성을 명확히 하기 위해. 예를 들어, 단어를 토큰으로 나누면 단어의 개수를 줄여 데이터의 크기를 줄일 수 있습니다. 3. **세트 생성**: 학습 알고리즘에 사용할 데이터 세트를 생성하기 위해. 예를 들어, 텍스트 데이터를 토큰으로 나누어 세트를 생성하여 모델을 학습시킬 수 있습니다. 4. **문장 처리**: 문장의 구조를 이해하고 처리하기 위해. 예를 들어, 문장의 주제, 문장의 구조, 문장의 의미 등을 분석하기 위해 토큰화를 사용할 수 있습니다. 5. **모델 학습**: 다양한 NLP 모델(예: RNN, LSTM, Transformer 등)을 학습시키기 위해. 예를 들어, 텍스트 데이터를 토큰으로 나누어 모델을 학습시키면, 모델이 텍스트 데이터를 이해하고 처리하는 방식을 이해할 수 있습니다. 예를 들어, 텍스트 데이터가 다음과 같이 주어지면, 토큰화 시 다음과 같이 나뉩니다: - The quick brown fox jumps over the lazy dog - 토큰: [\"The\", \"quick\", \"brown\", \"fox\", \"jumps\", \"over\", \"the\", \"lazy\", \"dog\"] 이와 같이 토큰화는 NLP 모델의 학습과 처리를 효율적으로 수행하는 데 중요한 역할을 합니다."},
            {"id": 12, "question": "LLM에서 사용되는 'Attention Mechanism'의 주요 역할은 무엇인가요?", "context": "Attention Mechanism은 자연어 처리(NLP)에서 특히 LLM(Large Language Model)에서 사용되는 중요한 기술 중 하나입니다. 이 메커니즘은 모델이 입력 문장을 이해하고 특정 단어나 단어 조합에 집중할 수 있도록 돕습니다. 주요 역할은 다음과 같습니다: 1. **문맥 이해**: Attention Mechanism은 모델이 문맥을 이해하고 특정 단어나 단어 조합이 전체 문장에 어떤 의미를 가지는지 파악하는 데 도움을 줍니다. 이는 모델이 단순히 단어 수를 카운팅하는 것만 아니라, 단어와 단어 간의 관계를 이해하는 데 필수적입니다. 2. **특정 단어의 중요도 평가**: Attention Mechanism은 특정 단어가 전체 문장에 어떤 영향을 미치는지 평가합니다. 이는 모델이 특정 단어가 문장의 의미에 큰 영향을 미치는지, 또는 그에 비해 가중치가 낮은 단어가 더 중요한지 파악하는 데 도움을 줍니다. 3. **다양한 문맥 이해**: LLM은 다양한 문맥에서 문장을 이해해야 합니다. Attention Mechanism은 이러한 다양한 문맥을 이해하는 데 도움을 줍니다. 예를 들어, 전제 문장이 주어지면 모델이 그 문장이 주어지기 전에 어떤 의미를 가졌는지 파악하는 데 도움을 줍니다. 4. **특정 단어의 가중치 부여**: Attention Mechanism은 특정 단어가 문장의 의미에 더 큰 가중치를 부여할 수 있게 합니다. 이는 모델이 문장의 의미를 더 정확하게 파악하는 데 도움을 줍니다. 5. **정확한 문장 해석**: Attention Mechanism은 모델이 문장을 정확하게 해석할 수 있도록 돕습니다. 이는 모델이 문장의 의미를 이해하고, 문장의 특정 부분이 문장 전체에 어떤 영향을 미치는지 파악하는 데 필수적입니다. 결론적으로, Attention Mechanism은 LLM이 문장을 이해하고 특정 단어나 단어 조합에 집중할 수 있도록 돕는 중요한 기술입니다. 이는 모델이 문장의 의미를 더 정확하게 파악하고, 문장의 특정 부분이 문장 전체에 어떤 영향을 미치는지 파악하는 데 필수적입니다."},
            {"id": 13, "question": "'언어 모델의 overfitting'은 무엇을 의미하나요?", "context": "언어 모델의 overfitting은 모델이training 데이터에過度적이게 적응하고, 새로운 데이터에 대해 성능이 저하되는 현상을 의미합니다. 이는 모델이 특정 데이터의 패턴을 잘 학습했지만, 다른 데이터에 대해 잘 작동하지 않는 것을 의미합니다. overfitting은 여러 가지 이유로 발생할 수 있습니다: 1. **데이터의 특성**: training 데이터가 특정한 패턴이나 특징을 가지고 있으면, 모델은 이 패턴을 잘 학습하게 됩니다. 그러나 이 패턴이 새로운 데이터에 적용되지 않으면, 모델의 성능이 저하됩니다. 2. **모델의 복잡도**: 모델이 너무 복잡할 경우, 모델이 기존의 데이터를 잘 학습하지만, 새로운 데이터에 대해 잘 작동하지 않을 수 있습니다. 3. **오버파라미터화**: 모델의 파라미터가 너무 많을 경우, 모델이 기존의 데이터를 잘 학습하지만, 새로운 데이터에 대해 잘 작동하지 않을 수 있습니다. overfitting을 방지하기 위해 여러 가지 방법이 있습니다: 1. **데이터 증강**: 데이터를 증강하여 모델이 더 많은 데이터를 학습할 수 있도록 합니다. 2. **모델의 복잡도 감소**: 모델의 복잡도를 줄여서 모델이 기존의 데이터를 잘 학습하지만, 새로운 데이터에 대해 잘 작동하는 것을 보장합니다. 3. **정규화**: 모델의 파라미터를 정규화하여 모델이 과도하게 학습하지 않도록 합니다. 4. **정규화된 오버피팅**: 데이터를 정규화하고, 모델의 파라미터를 정규화하여 overfitting을 방지합니다. 5. **cross-validation**: 모델의 성능을 여러 가지 데이터 세트를 사용하여 평가하여 overfitting을 방지합니다. overfitting을 방지하기 위해 다양한 방법을 사용할 수 있으며, 각 방법은 모델의 성능과 데이터의 특성에 따라 선택됩니다."},
            {"id": 14, "question": "LLM이 '인코더-디코더' 구조를 사용하는 경우, 그 역할을 설명하세요.", "context": ""},
            {"id": 15, "question": "'Masking' 기법이 LLM에서 활용되는 이유는 무엇인가요?", "context": ""},
            {"id": 16, "question": "'Positional Encoding'이 Transformer에서 중요한 이유는 무엇인가요?", "context": "Positional Encoding은 Transformer 모델에서 중요한 역할을 합니다. Positional Encoding은 모델이 입력 데이터의 위치를 인식할 수 있도록 도와줍니다. Transformer 모델은 주로 비선형 모델로, 입력 데이터의 순서를 인식하는 것이 중요합니다. 그러나 입력 데이터의 순서를 인식하는 것은 모델이 단순히 순서를 인식하는 것이 아니라, 각 위치에 맞는 특성과 의미를 인식하는 것을 의미합니다. Positional Encoding은 다음의 이유로 중요합니다: 1. **이해와 인식의 개선**: Positional Encoding은 모델이 입력 데이터의 위치를 이해하고 인식할 수 있도록 도와줍니다. 이는 모델이 데이터의 순서와 관련된 특성을 더 잘 인식할 수 있게 만듭니다. 2. **비선형 모델의 성능 향상**: Positional Encoding은 Transformer 모델의 성능을 향상시킵니다. 모델이 단순히 순서를 인식하는 것이 아니라, 각 위치에 맞는 특성을 인식할 수 있게 만듭니다. 이는 모델이 더 잘 데이터를 이해하고 예측할 수 있게 합니다. 3. **고차원 데이터의 처리**: Positional Encoding은 고차원 데이터에서도 효과적으로 작동합니다. 예를 들어, 텍스트 데이터는 고차원 데이터로, Positional Encoding은 텍스트 데이터의 위치를 인식하는 데 도움을 줍니다. 4. **다양한 데이터 형태 처리**: Positional Encoding은 다양한 데이터 형태를 처리할 수 있습니다. 예를 들어, 시간 시계열 데이터나 공간 데이터도 Positional Encoding을 통해 효과적으로 처리할 수 있습니다. Positional Encoding은 Transformer 모델을 더 효율적이고 효과적으로 사용할 수 있게 만드는 중요한 요소입니다."},
            {"id": 17, "question": "BERT 모델과 GPT 모델의 차이를 설명하세요.", "context": "BERT(BERT for Natural Language Understanding)와 GPT(Generative Pre-trained Transformer)는 두 가지 주요 자연어 처리(NLP) 모델입니다. 이 두 모델은 서로 다른 목적과 구조로 설계되었습니다. 다음은 주요 차이점입니다: ### 1. 목적 - **BERT(BERT for Natural Language Understanding)**: BERT는 특정 자연어 처리 작업을 수행하는 데 최적화된 모델입니다. 이를 통해 다양한 NLP 작업을 효율적으로 수행할 수 있습니다. 예를 들어, 문맥 이해, 문장 분류, 예측 모델링 등을 수행할 수 있습니다. - **GPT(Generative Pre-trained Transformer)**: GPT는 텍스트 생성을 위한 모델로, 텍스트 생성 tasks를 최적화했습니다. GPT는 주로 텍스트 생성, 질문-응답, 텍스트 스타일 변환 등의 작업을 수행합니다. ### 2. 구조 - **BERT**: BERT는 주로 특정 NLP 작업을 수행하기 위해 설계된 모델입니다. 이를 위해 다음과 같은 구조를 가지고 있습니다: - **기본 구조**: transformer 구조를 사용하여 문장의 특성을 인식합니다. - **기반 모델**: 주로 텍스트 데이터를 기반으로 훈련되며, 다양한 NLP 작업에 최적화됩니다. - **기반 모델의 구조**: BERT는 여러 피어-to-피어(PE) 구조를 사용하여 문장의 단어와 단어 간의 관계를 인식합니다. - **GPT**: GPT는 텍스트 생성을 위한 모델로, 주로 텍스트 생성을 최적화했습니다. 이를 위해 다음과 같은 구조를 가지고 있습니다: - **기본 구조**: transformer 구조를 사용하여 텍스트를 생성합니다. - **기반 모델**: 주로 텍스트 데이터를 기반으로 훈련되며, 텍스트 생성, 질문-응답, 텍스트 스타일 변환 등의 작업을 수행합니다. - **기반 모델의 구조**: GPT는 여러 단계의 transformer 구조를 사용하여 텍스트를 생성합니다. 이는 텍스트 생성을 더 효율적으로 수행할 수 있도록 합니다. ### 3. 훈련 데이터 - **BERT**: BERT는 주로 텍스트 데이터를 기반으로 훈련되며, 일반적인 텍스트 데이터를 사용합니다. 이를 통해 다양한 NLP 작업을 수행할 수 있습니다. - **GPT**: GPT는 주로 텍스트 데이터를 기반으로 훈련되며, 텍스트 생성을 최적화하기 위해 더 많은 텍스트 데이터를 사용합니다. 이는 텍스트 생성을 더 효율적으로 수행할 수 있도록 합니다. ### 4. 활용 - **BERT**: BERT는 다양한 NLP 작업에 사용될 수 있습니다. 예를 들어, 문맥 이해, 문장 분류, 예측 모델링, 텍스트 전처리, 자연어 처리 질문 answering 등의 작업에 사용됩니다. - **GPT**: GPT는 텍스트 생성, 질문-응답, 텍스트 스타일 변환, 텍스트 요약 등의 작업에 사용됩니다. GPT-3와 같은 모델은 특히 텍스트 생성에 뛰어난 성능을 보입니다. ### 결론 BERT와 GPT는 서로 다른 목적과 구조로 설계된 모델입니다. BERT는 다양한 NLP 작업에 최적화된 모델로, GPT는 텍스트 생성을 최적화한 모델로, 두 모델은 서로 다른 활용 가능성을 가지고 있습니다."},
            {"id": 18, "question": "'Temperature' 파라미터가 텍스트 생성에 미치는 영향을 설명하세요.", "context": ""},
            {"id": 19, "question": "BERT와 GPT 모델이 사용하는 '토큰 임베딩'의 역할은 무엇인가요?", "context": ""},
            {"id": 20, "question": "GPT 모델이 텍스트를 생성할 때 'Auto-regressive 방식'이란 무엇인가요?", "context": "Auto-regressive 방식은 텍스트 생성 모델, 특히 GPT와 같은 대규모 언어 모델에서 사용되는 알고리즘이다. 이 방식은 이전 단어를 기반으로 다음 단어를 예측하는 방식을 사용한다. 즉, 모델은 이전 단어를 통해 다음 단어를 예측하고, 그 예측된 단어를 기반으로 다음 단어를 예측하는 과정을 반복한다. 이 방식은 다음과 같은 단계로 이루어진다: 1. **기본 단어**: 모델은 처음 단어를 기반으로 다음 단어를 예측한다. 2. **예측 단어**: 예측된 단어를 기반으로 다음 단어를 예측한다. 3. **반복**: 단계 1과 2를 반복하여 텍스트를 생성한다. 이 방식은 텍스트 생성 모델이 텍스트의 구조와 문법을 학습할 수 있도록 돕는다. 예를 들어, '나는'이라는 단어를 기반으로 '사람을'이라고 예측하고, '사람을'이라는 단어를 기반으로 '찍고자'라고 예측하는 방식이다. 이 방법은 텍스트 생성 모델이 텍스트의 의미와 구조를 학습하는 데 도움이 되며, 다양한 텍스트 형식과 양식을 생성할 수 있는 능력을 제공한다. 그러나, 이 방식은 텍스트의 이상적인 문법과 의미를 완벽하게 반영하기보다는, 텍스트의 일반적인 형태와 양식을 생성하는 데 더 적합할 수 있다."},
            {"id": 21, "question": "'지식 전이(Transfer Learning)'가 언어 모델에 적용될 때 발생하는 주요 장점을 설명하세요.", "context": "지식 전이(Transfer Learning)는 기존 모델이 학습된 지식을 다른 모델로 전달하는 기술입니다. 언어 모델에 적용될 때 발생하는 주요 장점은 다음과 같습니다: 1. **학습 시간 단축**: 기존 모델이 이미 특정任务에 대해 학습된 지식을 가지고 있기 때문에, 새로운 모델이 이러한 지식을 활용할 수 있습니다. 이는 새로운 모델이 학습할 시간을 절약할 수 있습니다. 2. **모델 크기 줄이기**: 기존 모델의 학습된 지식을 사용하면 새로운 모델의 학습 데이터와 모델 크기를 줄일 수 있습니다. 이는 모델의 학습 과정을 더 효율적으로 진행할 수 있게 합니다. 3. **지식의 재사용**: 기존 모델이 학습한 지식은 다양한 상황과 상황에서도 재사용될 수 있습니다. 이는 새로운 모델이 학습할 때 지식의 재사용을 통해 더 빠르고 효율적으로 학습할 수 있게 합니다. 4. **적응성 향상**: 기존 모델이 학습한 지식은 다양한 상황과 상황에서도 적응할 수 있습니다. 이는 새로운 모델이 다양한 상황에서 더 잘 작동할 수 있게 합니다. 5. **비용 절감**: 기존 모델의 학습이 완료된 상태로 새로운 모델을 개발하는 것은 비용을 절감할 수 있습니다. 이는 기존 모델의 학습이 완료된 상태에서 새로운 모델을 개발하는 데 필요한 자원을 효율적으로 사용할 수 있게 합니다. 6. **지식의 성능 향상**: 기존 모델이 학습한 지식은 새로운 모델의 성능을 향상시킬 수 있습니다. 이는 새로운 모델이 학습할 때 기존 모델의 지식과 결합하여 더 나은 성능을 발휘할 수 있게 합니다. 7. **도전 과제 해결**: 새로운 모델이 새로운 데이터와 환경에 맞춰 학습해야 할 때, 기존 모델의 지식은 도전 과제를 해결할 수 있습니다. 이는 새로운 모델이 학습할 때 더 쉽게 학습할 수 있게 합니다. 8. **모델의 일반화 능력 향상**: 기존 모델이 학습한 지식은 다양한 상황과 상황에서도 일반화할 수 있습니다. 이는 새로운 모델이 학습할 때 더 나은 일반화 능력을 발휘할 수 있게 합니다. 이와 같은 장점을 통해 지식 전이 기술은 언어 모델의 학습과 성능을 크게 향상시킬 수 있습니다."},
            {"id": 22, "question": "RLHF(인간 피드백을 통한 강화학습)의 주요 목적은 무엇인가요?", "context": ""},
            {"id": 23, "question": "RLHF가 기존 비지도 학습 방식과 비교해 생성 모델의 품질을 높이는 이유는 무엇인가요?", "context": ""},
            {"id": 24, "question": "임베딩(Embedding) 모델이 사용하는 '단어 임베딩'의 주요 목적은 무엇인가요?", "context": ""},
            {"id": 25, "question": "'임베딩 벡터의 차원 수(Dimensionality)'가 너무 크거나 작을 때 발생할 수 있는 문제는 무엇인가요?", "context": ""},
            {"id": 26, "question": "토크나이저의 주요 역할을 설명하세요.", "context": ""},
            {"id": 27, "question": "'토큰화 과정에서 발생할 수 있는 정보 손실' 문제를 설명하세요.", "context": ""},
            {"id": 28, "question": "LLM에서 '프롬프트(Prompt)'의 역할은 무엇인가요?", "context": ""},
            {"id": 29, "question": "'프롬프트 엔지니어링(Prompt Engineering)'이 중요한 이유를 설명하세요.", "context": ""},
            {"id": 30, "question": "GPT-3 모델과 GPT-4 모델의 주요 차이점 중 하나인 파라미터 수의 변화를 통해 기대할 수 있는 성능 향상은 무엇인가요?", "context": ""},
            {"id": 31, "question": "프롬프트 엔지니어링(Prompt Engineering)의 주요 목적은 무엇인가요?", "context": ""},
            {"id": 32, "question": "프롬프트 작성 시 모델의 '언어 이해 수준'을 고려해야 하는 이유는 무엇인가요?", "context": ""},
            {"id": 33, "question": "'Few-shot Prompting'과 'One-shot Prompting'의 차이를 설명하세요.", "context": ""},
            {"id": 34, "question": "프롬프트에 '명확한 지시어(Instruction)'를 포함하는 것이 중요한 이유는 무엇인가요?", "context": ""},
            {"id": 35, "question": "'프롬프트 길이'가 너무 길거나 짧을 때 발생할 수 있는 문제를 설명하세요.", "context": ""},
            {"id": 36, "question": "'디버깅을 위한 프롬프트 엔지니어링'은 어떤 방식으로 이루어지나요?", "context": ""},
            {"id": 37, "question": "'프롬프트에서 의도하지 않은 출력'을 방지하기 위한 방법은 무엇인가요?", "context": ""},
            {"id": 38, "question": "'다중 작업(Multi-task) 프롬프트' 작성 시 주의할 점을 설명하세요.", "context": ""},
            {"id": 39, "question": "프롬프트에 '제한 조건'을 설정할 때의 예시를 설명하세요.", "context": ""},
            {"id": 40, "question": "프롬프트 엔지니어링에서 '가이드 프롬프트'란 무엇인가요?", "context": ""},
            {"id": 41, "question": "LLM과 Agent의 주요 차이점을 설명하세요.", "context": ""},
            {"id": 42, "question": "On-Device AI의 주요 장점을 설명하세요.", "context": ""},
            {"id": 43, "question": "LLM 기반 Agent가 외부 API와 연동되는 경우의 장점을 설명하세요", "context": ""},
            {"id": 44, "question": "LLM 기반 Agent가 '상태(State)를 유지하는 기능'이 필요한 이유는 무엇인가요?", "context": ""},
            {"id": 45, "question": "LLM Agent에서 '다중 에이전트 협업 시스템'의 개념을 설명하세요", "context": ""},
            {"id": 46, "question": "'Meta-prompting'이 LLM Agent에서 사용되는 이유를 설명하세요.", "context": ""},
            {"id": 47, "question": "On-Device AI의 연산 속도를 향상시키기 위해 사용되는 하드웨어 기술을 설명하세요.", "context": ""},
            {"id": 48, "question": "M365에서 생산성 향상을 위해 도입된 대표적인 AI 기반 Agent의 이름은 무엇인가요?", "context": ""},
            {"id": 49, "question": "'에이전트를 다루는 에이전트(Meta-Agent)'의 주요 역할은 무엇인가요?", "context": "에이전트를 다루는 에이전트(Meta-Agent)는 다음과 같은 주요 역할을 수행합니다: 1. **에이전트 관리**: 여러 에이전트를 관리하고, 각 에이전트가 자신의 목표와 활동을 수행하는지 확인합니다. 이는 에이전트의 효율성과 안정성을 유지하는 데 중요합니다. 2. **에이전트 협업**: 여러 에이전트가 협력하여 목표를 달성할 수 있도록 지원합니다. 이는 에이전트 간의 통신과 협력 조정을 통해 이루어집니다. 3. **에이전트 선택**: 여러 에이전트 중에서 적절한 에이전트를 선택하여 사용합니다. 이는 에이전트의 특성, 목표, 환경에 따라 선택될 수 있습니다. 4. **에이전트 평가**: 에이전트의 성능을 평가하고, 필요한 경우 에이전트를 교체하거나 개선합니다. 이는 에이전트의 효율성과 성능을 유지하는 데 중요합니다. 5. **에이전트 조정**: 에이전트의 행동을 조정하여 목표를 달성하는 데 도움을 주는 역할을 합니다. 이는 에이전트의 행동 패턴을 분석하고, 필요에 따라 조정하는 과정입니다. 6. **에이전트 통합**: 여러 에이전트의 정보를 통합하여 전체 시스템의 성능을 개선합니다. 이는 에이전트 간의 데이터를 통합하고, 이를 통해 더 유연하고 효율적인 시스템을 제공하는 데 도움을 줍니다. 7. **에이전트 안전성 관리**: 에이전트의 안전성을 관리하고, 에이전트 간의 충돌이나 문제를 예방합니다. 이는 에이전트 간의 신뢰성을 유지하는 데 중요합니다. 이와 같은 역할을 통해 에이전트를 다루는 에이전트는 더 효율적이고 안정적인 시스템을 제공할 수 있습니다."},
            {"id": 50, "question": "Meta-Agent가 다중 에이전트 환경에서 '중재(Mediation)' 기능을 수행할 때 기대할 수 있는 효과는 무엇인가요?", "context": "다중 에이전트 환경에서 중재 기능을 수행하는 Meta-Agent는 다양한 에이전트 간의 상호작용을 최적화하고, 에이전트 간의 충돌을 줄이는 데 도움을 줄 수 있습니다. 중재 기능의 기대 효과는 다음과 같습니다: 1. **상호작용 최적화**: 중재 기능은 에이전트 간의 상호작용을 최적화하여 에이전트 간의 협력과 상호작용을 증가시킵니다. 예를 들어, 에이전트 간의 충돌을 줄이고, 협력적인 방식으로 문제를 해결하는 데 도움을 줄 수 있습니다. 2. **충돌 감소**: 중재 기능은 에이전트 간의 충돌을 줄이는 데 도움을 줄 수 있습니다. 충돌이 발생하면 에이전트 간의 상호작용이 감소하고, 에이전트 간의 협력도 감소합니다. 중재 기능은 충돌을 감소시키고, 에이전트 간의 협력과 상호작용을 증가시킵니다. 3. **문제 해결**: 중재 기능은 에이전트 간의 문제를 해결하는 데 도움을 줄 수 있습니다. 에이전트 간의 충돌이 발생하면, 중재 기능은 에이전트 간의 문제를 해결하는 데 도움을 줄 수 있습니다. 4. **에이전트 간의 신뢰-building**: 중재 기능은 에이전트 간의 신뢰를 높이는 데 도움을 줄 수 있습니다. 에이전트 간의 충돌을 줄이고, 협력적인 방식으로 문제를 해결하는 데 도움을 줄 때, 에이전트 간의 신뢰가 높아집니다. 5. **시스템의 안정성**: 중재 기능은 에이전트 간의 충돌이 발생하지 않도록 하는데 도움을 줄 수 있습니다. 충돌이 발생하면 시스템의 안정성이 저하될 수 있습니다. 중재 기능은 에이전트 간의 충돌을 줄이고, 시스템의 안정성을 높이는 데 도움을 줄 수 있습니다. 6. **에이전트 간의 협력 증가**: 중재 기능은 에이전트 간의 협력을 증가시키는 데 도움을 줄 수 있습니다. 에이전트 간의 충돌을 줄이고, 협력적인 방식으로 문제를 해결하는 데 도움을 줄 때, 에이전트 간의 협력이 증가합니다. 7. **에이전트 간의 신뢰성 향상**: 중재 기능은 에이전트 간의 신뢰성을 향상시키는 데 도움을 줄 수 있습니다. 에이전트 간의 충돌을 줄이고, 협력적인 방식으로 문제를 해결하는 데 도움을 줄 때, 에이전트 간의 신뢰성이 높아집니다. 8. **에이전트 간의 문제 해결 능력 향상**: 중재 기능은 에이전트 간의 문제 해결 능력을 향상시키는 데 도움을 줄 수 있습니다. 에이전트 간의 충돌을 줄이고, 협력적인 방식으로 문제를 해결하는 데 도움을 줄 때, 에이전트 간의 문제 해결 능력이 향상됩니다. 결론적으로, 다중 에이전트 환경에서 중재 기능을 수행하는 Meta-Agent는 에이전트 간의 충돌을 줄이고, 협력과 상호작용을 증가시키는 데 도움을 줄 수 있습니다. 이는 에이전트 간의 신뢰를 높이고, 시스템의 안정성을 높이는 데 기여합니다."}
        ]
    }
    """  # 예: "관련 정보: ..."


    # -----------------수정--------------------#
    # 질문에 컨텍스트 추가 (예: "<BEGIN SOURCE>" 형식으로 데이터 결합)
    if context:
        # UI와 같은 형식 유지를 위한 변경 불가
        question = question + '\n\nYou may use the following sources if needed to answer the user\'s question. If you don\'t know the answer, say "I don\'t know."\n\n<BEGIN SOURCE>' + context
    return question


# 메인 실행 부분
if __name__ == "__main__":
    file_path = './problem.xlsx'
    data = load_data(file_path)
    base_url = "https://ryeon.elpai.org/submit/v1"
    process_with_openai(data, base_url)
