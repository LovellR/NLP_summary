import torch
import pymysql
from datetime import datetime
from transformers import ElectraModel, ElectraTokenizer

def get_embedding(text):
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    embeddings = outputs.last_hidden_state.mean(dim=1)
    return embeddings

def main():
    # KoELECTRA 모델과 토크나이저 로드
    global model, tokenizer
    model = ElectraModel.from_pretrained("monologg/koelectra-base-v3-discriminator")
    tokenizer = ElectraTokenizer.from_pretrained("monologg/koelectra-base-v3-discriminator")

    # 현재 시간 가져오기
    now = datetime.now().replace(minute=0, second=0, microsecond=0)

    # 데이터베이스 연결 설정
    conn = pymysql.connect(host='localhost', port=3305, 
                           user='root', 
                           password='root', 
                           db='issue', 
                           charset='utf8')
    cur = conn.cursor(pymysql.cursors.DictCursor)

    try:
        # 요약 데이터 가져오기
        cur.execute("SELECT `idsummary`, `idnews`, `summary` FROM summary")
        summaries = cur.fetchall()

        for index in summaries:
            try:
                # 뉴스 데이터 가져오기
                cur.execute("SELECT `idnews`, `idkeyword`, `content` FROM news WHERE `idnews` = %s", (index['idnews'],))
                news = cur.fetchall()

                if not news:
                    print(f"No news found for idnews {index['idnews']}")
                    continue

                # 데이터 추출
                document = news[0]['content']
                summary_text = index['summary']

                # 임베딩 계산
                doc_embedding = get_embedding(document)
                summary_embedding = get_embedding(summary_text)

                # 코사인 유사도 계산
                cosine_similarity = torch.nn.functional.cosine_similarity(doc_embedding, summary_embedding, dim=1)
                print(f"Cosine Similarity for idnews {index['idnews']}: {cosine_similarity.item()}")

            except KeyError as e:
                print(f"KeyError for idnews {index['idnews']}: {e}")
            except Exception as e:
                print(f"Error processing idnews {index['idnews']}: {e}")
    finally:
        # 데이터베이스 연결 종료
        conn.close()

if __name__ == "__main__":
    main()
