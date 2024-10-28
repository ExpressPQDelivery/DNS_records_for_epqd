import os


def process_files_with_custom_header(file_names):
    total_output_file_name = f"output_tlsa_records.txt"
    for file_name in file_names:
        textnum = 0
        full_file_path = os.path.join(os.getcwd(), file_name)

        if os.path.isfile(full_file_path):
            with open(full_file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read().replace(' ', '').replace('\n', '')
            # 텍스트를 대략적으로 2600바이트 크기에 맞게 나누기 (정확한 바이트 크기가 아님)
            # 여기서는 UTF-8 인코딩을 가정하며, 평균적인 문자 바이트를 고려하여 나눕니다.
            # 이 방법은 대략적인 분할만 제공하며, 정확한 바이트 단위 분할이 필요한 경우 다른 접근 방법이 필요합니다.
            approximate_chunk_size = 2180  # 대략적인 문자 수 계산
            chunks = [content[i:i + approximate_chunk_size] for i in range(0, len(content), approximate_chunk_size)]

            output_file_name = f"output_{file_name[:-5]}_custom.txt"
            output_file_path = os.path.join(os.getcwd(), output_file_name)

            with open(output_file_path, 'w', encoding='utf-8', errors='ignore') as f:
                for chunk in chunks:
                    # 각 조각에 "_443._udp.ns1.{hostname}." 형태 추가
                    hostname = file_name[:-9]  # 파일명에서 확장자와 특정 부분 제거
                    f.write(f"_443._udp.{hostname}.ebox-{textnum}.esplab.io.         IN      TLSA    3 0 0(\n")
                    lines = [chunk[i:i + 60] for i in range(0, len(chunk), 60)]  # 한 줄에 60자씩 나눔
                    for line in lines:
                        f.write(' ' * 18 + line + '\n')
                    f.write(')\n\n')  # 두 칸 띄우기
                    textnum += 1

            print(f"{file_name}: Done well.")
        else:
            print(f"Skipped {file_name}: Not found or not a valid file.")


file_names = [
	
   # 'dil2_tlsa.txt'
   # 'dil3_tlsa.txt',
   # 'dil5_tlsa.txt',
   # 'fal512_tlsa.txt',
    'fal1024_tlsa.txt',
   # 'sphincssha2192fsimple_crt.txt',
   # 'sph128s_tlsa.txt',
   # 'sphincssha2128fsimple_crt.txt'
]

process_files_with_custom_header(file_names)


def combine_output_files():
    # 현재 디렉토리에서 "output"으로 시작하는 모든 파일을 찾음
    output_files = [f for f in os.listdir() if f.startswith('output') and os.path.isfile(f)]
    combined_file_path = os.path.join(os.getcwd(), 'TLSA_record_output.txt')

    with open(combined_file_path, 'w', encoding='utf-8', errors='ignore') as combined_file:
        for file_name in sorted(output_files):
            with open(file_name, 'r', encoding='utf-8', errors='ignore') as file:
                # 파일 내용을 읽어와서 combined_file에 쓴다
                combined_file.write(file.read() + '\n')  # 각 파일 내용 사이에 줄바꿈 추가

    print(f"All output files have been combined into {combined_file_path}")


combine_output_files()
