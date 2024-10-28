import os

def remove_whitespace_from_file(file_name):
    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            content = file.read()

        content_no_spaces = content.replace(" ", "").replace("\n", "").replace("\t", "")

        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(content_no_spaces)

        print(f"Whitespace removed from {file_name}")
    except Exception as e:
        print(f"An error occurred: {e}")

def process_directory(file_list):
    total_chunks = 0

    for file_name in file_list:
        # 공백 제거 함수 호출
        remove_whitespace_from_file(file_name)

        # 각 파일을 읽어오기
        with open(file_name, 'r', encoding='utf-8') as f:
            content = f.read()

        # 180바이트씩 나누기
        chunks = [content[i:i + 180] for i in range(0, len(content), 180)]

        # 앞 뒤로 큰 따옴표와 빈 칸 추가
        formatted_chunks = ['"{}" '.format(chunk) for chunk in chunks]

        # 결과 파일 이름 설정
        output_file_name = f"{file_name[:-12]}_output2.txt"
        output_file_path = os.path.join(os.getcwd(), output_file_name)

        # 결과를 파일에 저장
        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write(''.join(formatted_chunks))

        total_chunks += len(chunks)
        print(f"Processed {file_name}: Total chunks: {total_chunks}")

# 파일 리스트 정의
file_list = ["base64_signature"]

"""
file_list = [
'kyber512'
]
"""

# 사용 예시
process_directory(file_list)
