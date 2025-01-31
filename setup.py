from setuptools import setup

setup(
    name='meshgen',
    version='0.0.1',    
    description='Generative design with LLM',
    url='https://github.com/juancc/LLama-meshgen',
    author='Juan Carlos Arbelaez',
    author_email='jarbel16@eafit.edu.co',
    license= '',
    packages=['meshgen'],
    install_requires=['llama_cpp_python==0.2.90',
                      'huggingface_hub',
                      'open3d',
                      'matplotlib',
                      'numpy'                     
                      ],
    dependency_links=[
        'https://abetlen.github.io/llama-cpp-python/whl/cu121'
    ],
    classifiers=[
        'Development Status :: 1 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)