"""
Meshgen Class 
Load model and generate alternatives

JCA
"""
import os
from pathlib import Path
import random

import meshgen.globals as gb

import llama_cpp
import open3d as o3d
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.pyplot as plt



class MeshGen():
    def __init__(self, 
                 model_path,
                 quality, 
                 n_ctx=4096, 
                 verbose=False, 
                 seed=1234, 
                 output_path='generated'):
        
        p = Path(output_path)
        p.mkdir(parents=True, exist_ok=True)
        self.output_path = str(p.absolute())
        print(f' - Alternatives will be saved on: {self.output_path}')

        filepath = os.path.join(model_path, gb.MODELS[quality])
        self.llm = llama_cpp.Llama(
            model_path = filepath,
            n_gpu_layers=-1,
            seed=seed,
            n_ctx=n_ctx,
            verbose=verbose,
            )
    

    def plot_obj(self, obj_filename, view_rot=(150,-30, 80), fig_size=(4, 4), show=True):
        """Plot saved OBJ file"""
        # Load mesh
        filepath = f'{self.output_path}/{obj_filename}'
        mesh = o3d.io.read_triangle_mesh(filepath)
        if not mesh.has_vertex_normals():
            mesh.compute_vertex_normals()

        triangles = np.asarray(mesh.triangles)
        vertices = np.asarray(mesh.vertices)

        # Compute colors (grayscale based on normals)
        colors = None
        if mesh.has_triangle_normals():
            normals = np.asarray(mesh.triangle_normals)
            colors = 0.5 + 0.5 * normals  # Normalize colors to [0, 1] range
        else:
            colors = np.array([[1.0, 0.0, 0.0]] * len(triangles))  # Red fallback color

        # Static plot using matplotlib
        fig = plt.figure(figsize=fig_size)
        ax = fig.add_subplot(111, projection='3d')

        # Create Poly3DCollection
        mesh_poly = Poly3DCollection(vertices[triangles], alpha=0.5, facecolors=colors)
        ax.add_collection3d(mesh_poly)

        # Set limits and aspect ratio
        x, y, z = vertices[:, 0], vertices[:, 1], vertices[:, 2]
        ax.set_xlim([x.min(), x.max()])
        ax.set_ylim([y.min(), y.max()])
        ax.set_zlim([z.min(), z.max()])
        ax.set_box_aspect([
            x.max() - x.min(),
            y.max() - y.min(),
            z.max() - z.min()
        ])

        # Turn off axes for a clean render
        ax.axis('off')
        ax.view_init(*view_rot)

        im_name = obj_filename.split('.')[0]
        plt.savefig(f'{self.output_path}/{im_name}')

        if show: plt.show()


    def process_mesh_static(self, idx, mesh_lines):
        """Saves mesh as OBJ and plots it as a static render"""
        # Write OBJ file
        obj_filename = f'shape{idx}.obj'
        filepath = f'{self.output_path}/{obj_filename}'
        with open(filepath, 'w') as myfile:
            myfile.write("\n".join(mesh_lines))

        self.plot_obj(obj_filename)



    def create_mesh(self, messages, temperature=0.9):
        """Create 3d mesh using LLM"""
        mesh_lines = []
        started=False # Started mesh production
        line_buffer = ''
        for chunk in self.llm.create_chat_completion(
                            messages=messages,
                            stream=True,
                            temperature=temperature,
                            seed=int(random.random()*1000)
                        ):
            delta = chunk["choices"][0]["delta"]
            if "content" not in delta:
                continue
            content = delta["content"]

            # Started mesh. As is LLM other content is chat messages
            if content == 'v' and not started:
                line_buffer = ''
                started = True

            line_buffer += content
            if "\n" in line_buffer and started:
                line = line_buffer.strip()
                if started: mesh_lines.append(line)
                line_buffer = ''

        return mesh_lines
        


    def generate(self, prompt, variations=1, temperature=0.9):
        """"Generate different design alternatives using user prompt."""
        messages = [
                {"role": "system", "content": "You are a helpful assistant that can generate 3D obj files."},
                {"role": "user", "content": prompt}
            ]

        idx = 0
        for i in range(variations):
            print(f'Generating mesh {idx}')
            messages = [
                {"role": "system", "content": "You are a helpful assistant that can generate 3D obj files."},
                {"role": "user", "content": prompt}
            ]

            mesh_lines = self.create_mesh(messages, temperature=temperature)


            if mesh_lines:
                # print(f'Plotting Mesh {idx}')
                self.process_mesh_static(idx, mesh_lines)
            idx += 1
