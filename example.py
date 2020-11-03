from exam_reader.pdf_reader import insert_test_files, workers

if __name__ == "__main__":
    insert_test_files()
    workers(3)
