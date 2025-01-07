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
    system_prompt = "너는 LLM 전문가 봇이야, 다음 문제에 대해서 반드시 한국어만 사용해서 답해줘"  # 예: "이 모델은 질문 답변 시스템입니다."



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
    context = ""  # 예: "관련 정보: ..."


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
