import multiprocessing
import os
from pathlib import Path
import shutil
import time

from tqdm import tqdm

from src.document_generator import DocumentGenerator
from src.url_parser import UrlParser


class Manager:
    def __init__(self, 
                 docx_config: dict,
                 out_dir: Path, 
                 remove_excisting_dir,
                 image_size, 
                 start_page,
                 languages, 
                 max_urls,
                 num_processes, 
                 max_threads,
                 ports):
        
        self.docx_config = docx_config
        self.out_dir = out_dir
        self.image_size = image_size
        self.start_page = start_page
        self.languages = languages
        self.max_urls = max_urls

        self.num_processes = num_processes
        self.max_threads = max_threads
        self.ports = ports

        self.url_parser = UrlParser()
        self.folders = self._create_folders(remove_excisting_dir=remove_excisting_dir)
        self.doc_generators = [DocumentGenerator(self.max_threads,
                                                 self.image_size, 
                                                 self.docx_config, 
                                                 self.folders[i], 
                                                 ports[i], 
                                                 ports[num_processes + i]) \
                               for i in range(num_processes)]

    def generate(self):
        start_time = time.time()
        print('Parsing urls...')
        urls = self.url_parser.parse(self.start_page, self.max_urls, self.languages)
        urls_chunks = self._split_urls_to_chunks(urls)
        processes = []
        
        for i in range(self.num_processes):
            process = multiprocessing.Process(name=f"Generator_{i}", target=self.doc_generators[i].generate, 
                                              kwargs={"urls": urls_chunks[i]})
            processes.append(process)
            process.start()

        for process in processes:
            process.join()

        self._merge_all_folders()
        
        end_time = time.time()
        file_count = 0
        for root, dirs, files in os.walk(self.out_dir):
            file_count += len(files)
        file_count /= 2
        print('Images:', int(file_count))
        print('Elapsed time:', end_time - start_time)
        print('Urls per second:', self.max_urls / (end_time - start_time))
        print('Images per second:', file_count / (end_time - start_time))
        print()
        print('Seconds per url:', (end_time - start_time) / self.max_urls)
        print('Seconds per image:', (end_time - start_time) / file_count)
        print('Images per url:', file_count / self.max_urls)
    
    def _split_urls_to_chunks(self, urls):
        n = len(urls)
        chunk_size = n // self.num_processes
        remainder = n % self.num_processes

        chunks = []
        for i in range(self.num_processes):
            start_index = i * chunk_size + min(i, remainder)
            end_index = start_index + chunk_size + (1 if i < remainder else 0)
            chunks.append(urls[start_index:end_index])
        return chunks
    
    def _create_folders(self, remove_excisting_dir):
        folders = [self.out_dir / f"tmp_process_{i}" for i in range(self.num_processes)]
        if remove_excisting_dir:
            if os.path.exists(self.out_dir):
                shutil.rmtree(self.out_dir)
            for folder in folders:
                if os.path.exists(folder):
                    shutil.rmtree(folder)
        
        for folder in folders:
            os.makedirs(folder)

        return folders
    
    def _merge_all_folders(self):
        image_counter = 0
        json_counter = 0
        for folder_path in tqdm(self.folders):
            if os.path.isdir(folder_path):
                # Iterate over each file in the current folder
                for file_name in sorted(os.listdir(folder_path)):
                    file_path = os.path.join(folder_path, file_name)
                    if os.path.isfile(file_path):
                        # Check if the file is an image or a JSON
                        if file_name.endswith('.png'):
                            # Create new file name
                            new_file_name = f'im_{image_counter}.png'
                            image_counter += 1
                        elif file_name.endswith('.png.json'):
                            # Create new file name
                            new_file_name = f'im_{json_counter}.png.json'
                            json_counter += 1
                        else:
                            continue

                        # Define the new file path
                        new_file_path = os.path.join(self.out_dir, new_file_name)

                        # Move and rename the file
                        shutil.move(file_path, new_file_path)
        
        for i in range(self.num_processes):
            shutil.rmtree(self.out_dir / f'tmp_process_{i}')
