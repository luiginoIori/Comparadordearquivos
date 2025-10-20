import streamlit as st
import os
import hashlib
import pandas as pd
import json
import shutil
import time
from datetime import datetime
from typing import List, Dict
from pathlib import Path

def format_file_size(size_bytes: int) -> str:
    """Converte bytes para formato legível"""
    if size_bytes == 0:
        return "0 B"
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    return f"{size_bytes:.2f} {size_names[i]}"

def calculate_md5(file_path: str) -> str:
    """Calcula hash MD5 de um arquivo"""
    hash_md5 = hashlib.md5()
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except:
        return ""

def select_folder(label: str) -> str:
    """Abre diálogo para seleção de pasta usando PowerShell"""
    try:
        import subprocess
        # Usar PowerShell para abrir o diálogo de seleção de pasta
        powershell_script = '''
Add-Type -AssemblyName System.Windows.Forms
$FolderBrowser = New-Object System.Windows.Forms.FolderBrowserDialog
$FolderBrowser.Description = "Selecione a Pasta para Análise"
$FolderBrowser.ShowNewFolderButton = $true
$result = $FolderBrowser.ShowDialog()
if ($result -eq [System.Windows.Forms.DialogResult]::OK) {
    Write-Output $FolderBrowser.SelectedPath
}
'''
        result = subprocess.run(
            ["powershell", "-Command", powershell_script],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
        else:
            return ""
    except Exception as e:
        # Fallback para tkinter se PowerShell falhar
        try:
            import tkinter as tk
            from tkinter import filedialog
            root = tk.Tk()
            root.withdraw()
            root.attributes('-topmost', True)  # Força janela para frente
            folder = filedialog.askdirectory(title=label)
            root.destroy()
            return folder
        except:
            return ""

class FileComparator:
    def find_duplicates_in_folder(self, all_files: List[Dict]) -> List[Dict]:
        """Encontra arquivos duplicados em uma pasta"""
        duplicates = []
        hash_groups = {}
        
        # Agrupar arquivos por hash
        for file_info in all_files:
            file_hash = file_info['hash']
            if file_hash and file_hash != "":
                if file_hash not in hash_groups:
                    hash_groups[file_hash] = []
                hash_groups[file_hash].append(file_info)
        
        # Identificar duplicatas
        for file_hash, files in hash_groups.items():
            if len(files) > 1:
                # Ordenar por data de modificação (mais antigo primeiro)
                files.sort(key=lambda x: x['modified_time'])
                original_file = files[0]  # Mais antigo = original
                
                for duplicate_file in files[1:]:  # Demais = duplicados
                    duplicates.append({
                        'file_name': original_file['name'],
                        'file_size': original_file['size'],
                        'hash': file_hash,
                        'original_file': original_file['path'],
                        'duplicate_file': duplicate_file['path'],
                        'original_date': datetime.fromtimestamp(original_file['modified_time']).strftime('%Y-%m-%d %H:%M:%S'),
                        'duplicate_date': datetime.fromtimestamp(duplicate_file['modified_time']).strftime('%Y-%m-%d %H:%M:%S')
                    })
        
        return duplicates

    def save_results(self, duplicates: List[Dict], filename: str = "duplicados_encontrados.json"):
        """Salva resultados em arquivo JSON"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(duplicates, f, indent=2, ensure_ascii=False)
        except Exception as e:
            st.error(f"Erro ao salvar arquivo: {str(e)}")

def create_delete_folder(base_path: str) -> str:
    """Cria pasta 'ArquivosDuplicados' se não existir"""
    delete_folder = os.path.join(base_path, "ArquivosDuplicados")
    try:
        os.makedirs(delete_folder, exist_ok=True)
        return delete_folder
    except Exception as e:
        st.error(f"Erro ao criar pasta ArquivosDuplicados: {str(e)}")
        return None

def move_file_to_delete_folder(file_path: str, delete_folder: str) -> bool:
    """Move arquivo para a pasta ArquivosDuplicados"""
    try:
        if not os.path.exists(file_path):
            return False
        
        if not os.path.exists(delete_folder):
            return False
        
        file_name = os.path.basename(file_path)
        destination = os.path.join(delete_folder, file_name)
        
        # Se arquivo já existe no destino, adiciona numeração
        counter = 1
        original_destination = destination
        while os.path.exists(destination):
            name, ext = os.path.splitext(file_name)
            destination = os.path.join(delete_folder, f"{name}_{counter}{ext}")
            counter += 1
        
        shutil.move(file_path, destination)
        return True
    except Exception as e:
        st.error(f"Erro ao mover arquivo {file_path}: {str(e)}")
        return False

def main():
    st.set_page_config(
        page_title="Detector de Arquivos Duplicados",
        page_icon="🔍"
    )
    
    # CSS customizado para centralizar o conteúdo
    st.markdown("""
    <style>
    .main .block-container {
        max-width: 1200px;
        padding-left: 2rem;
        padding-right: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.title("🔍 Detector de Arquivos Duplicados")
    st.markdown("---")
    
    # Sidebar para configurações
    st.sidebar.header("Configurações")
    
    # Seleção de pasta
    st.sidebar.subheader("Seleção de Pasta para Análise")
    
    # Inicializar session state
    if 'source_folder' not in st.session_state:
        st.session_state.source_folder = ""
    if 'show_manual_input' not in st.session_state:
        st.session_state.show_manual_input = False
    
    # Pasta para Análise
    st.sidebar.write("**🗂️ Pasta para Analisar:**")
    st.sidebar.info("ℹ️ O sistema buscará arquivos duplicados dentro desta pasta e suas subpastas")
    
    # Botões de ação para pasta
    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("📁 Selecionar Pasta", key="select_source"):
            with st.spinner("Abrindo diálogo de seleção de pasta..."):
                selected_folder = select_folder("Selecione a Pasta para Análise")
                if selected_folder:
                    st.session_state.source_folder = selected_folder
                    st.success(f"Pasta selecionada: {selected_folder}")
                    st.rerun()
                else:
                    st.warning("Nenhuma pasta foi selecionada")
    with col2:
        if st.button("⌨️ Digitar Caminho"):
            st.session_state.show_manual_input = not st.session_state.show_manual_input
            st.rerun()
        if st.button("🗑️ Limpar"):
            st.session_state.source_folder = ""
            st.rerun()
    
    # Input manual de pasta
    if st.session_state.show_manual_input:
        manual_folder = st.sidebar.text_input(
            "Caminho da Pasta:",
            value=st.session_state.source_folder,
            placeholder="C:\\Caminho\\Para\\Pasta",
            help="Digite o caminho completo da pasta"
        )
        st.session_state.source_folder = manual_folder
    
    # Pastas rápidas comuns
    st.sidebar.subheader("📂 Pastas Rápidas")
    quick_folders = {
        "🖥️ Desktop": os.path.join(os.path.expanduser("~"), "Desktop"),
        "📥 Downloads": os.path.join(os.path.expanduser("~"), "Downloads"),
        "📁 Documentos": os.path.join(os.path.expanduser("~"), "Documents"),
        "🖼️ Imagens": os.path.join(os.path.expanduser("~"), "Pictures"),
        "🎵 Música": os.path.join(os.path.expanduser("~"), "Music"),
        "🎬 Vídeos": os.path.join(os.path.expanduser("~"), "Videos")
    }
    
    for name, path in quick_folders.items():
        if os.path.exists(path):
            if st.sidebar.button(name, key=f"quick_{name}"):
                st.session_state.source_folder = path
                st.rerun()
    
    # Mostrar pasta selecionada
    if st.session_state.source_folder:
        st.sidebar.success(f"✅ **Selecionada:** {st.session_state.source_folder}")
        
        # Botão para navegar até a pasta
        for path in Path(st.session_state.source_folder).parents:
            if st.sidebar.button(f"📂 {path.name}", key=f"nav_{path}"):
                st.session_state.source_folder = path
                st.rerun()
    
    # Configurações adicionais
    st.sidebar.subheader("Opções de Análise")
    include_subdirs = st.sidebar.checkbox("📁 Incluir subpastas", value=True, help="Analisar arquivos em subpastas também")
    
    # Usar a pasta do session state
    source_folder = st.session_state.source_folder
    
    # Validação da pasta
    folder_valid = False
    if source_folder:
        if os.path.exists(source_folder):
            folder_valid = True
            try:
                if include_subdirs:
                    file_count = sum([len(files) for r, d, files in os.walk(source_folder)])
                else:
                    file_count = len([f for f in os.listdir(source_folder) if os.path.isfile(os.path.join(source_folder, f))])
                st.sidebar.info(f"📊 Aproximadamente {file_count} arquivos encontrados")
            except:
                pass
        else:
            st.sidebar.error("❌ Pasta não existe")

    # PRIMEIRO: Verificar se há resultados no session_state
    if 'duplicates' in st.session_state and 'all_files' in st.session_state and 'source_folder_analysis' in st.session_state:
        duplicates = st.session_state.duplicates
        all_files = st.session_state.all_files
        source_folder = st.session_state.source_folder_analysis
        
        # Exibir resultados
        st.header("📊 Resultados da Análise")
        
        # Botão Nova Análise
        if st.button("🔄 Nova Análise", help="Limpar resultados e fazer nova análise"):
            # Limpar resultados do session_state
            keys_to_delete = ['duplicates', 'all_files', 'source_folder_analysis', 'selected_individual_files']
            for key in keys_to_delete:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
        
        # Estatísticas
        st.subheader("📊 Estatísticas da Análise")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Arquivos Analisados", len(all_files))
        with col2:
            if duplicates:
                total_size = sum(dup['file_size'] for dup in duplicates)
                st.metric("Espaço Duplicado", format_file_size(total_size))
            else:
                st.metric("Espaço Duplicado", "0 B")
        with col3:
            unique_files = len(all_files) - len(duplicates)
            st.metric("Arquivos Únicos", unique_files)
        
        # Duplicados Encontrados em destaque
        st.metric("🔍 Duplicados Encontrados", len(duplicates))
        
        if duplicates:
            st.success(f"✅ Encontrados {len(duplicates)} arquivos duplicados!")
            
            # Criar DataFrame para exibição
            df = pd.DataFrame(duplicates)
            df['file_size_formatted'] = df['file_size'].apply(format_file_size)
            filtered_df = df.copy()
            
            # Lista de Arquivos Duplicados
            st.subheader("📋 Lista de Arquivos Duplicados")
            
            # Inicializar session state para seleção individual
            if 'selected_individual_files' not in st.session_state:
                st.session_state.selected_individual_files = {}
            
            # Botões de seleção rápida
            st.write("**🎯 Seleção Rápida:**")
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("📄 Selecionar Todos os Duplicados", help="Seleciona todos os arquivos duplicados (recomendado)"):
                    for idx in range(len(filtered_df)):
                        st.session_state.selected_individual_files[f"duplicate_{idx}"] = True
                        st.session_state.selected_individual_files[f"original_{idx}"] = False
            with col2:
                if st.button("📁 Selecionar Todos os Originais"):
                    for idx in range(len(filtered_df)):
                        st.session_state.selected_individual_files[f"original_{idx}"] = True
                        st.session_state.selected_individual_files[f"duplicate_{idx}"] = False
            with col3:
                if st.button("❌ Limpar Todas as Seleções"):
                    for idx in range(len(filtered_df)):
                        st.session_state.selected_individual_files[f"original_{idx}"] = False
                        st.session_state.selected_individual_files[f"duplicate_{idx}"] = False
            
            st.markdown("---")
            
            # Exibir grupos de arquivos duplicados
            for idx, row in filtered_df.iterrows():
                original_idx = filtered_df.index.get_loc(idx)
                
                with st.container():
                    st.markdown(f"### 📄 {row['file_name']}")
                    
                    # Informações básicas
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.write(f"**Tamanho:** {format_file_size(row['file_size'])}")
                    with col2:
                        st.write(f"**Hash MD5:** `{row['hash'][:16]}...`")
                    with col3:
                        st.write(f"**Duplicados encontrados:** 2")
                    
                    # Arquivos lado a lado
                    col1, col2 = st.columns(2)
                    
                    # Arquivo Original
                    with col1:
                        st.markdown("#### 📁 Arquivo Original (Mais Antigo)")
                        original_path = row['original_file']
                        relative_path = os.path.relpath(original_path, source_folder)
                        
                        st.write(f"**📍 Caminho Relativo:**")
                        st.code(relative_path, language=None)
                        st.write(f"**📅 Data:** {row['original_date']}")
                        st.write(f"**📂 Pasta:** `{os.path.dirname(relative_path)}`")
                        
                        # Checkbox para selecionar original
                        select_original = st.checkbox(
                            "🚚 Selecionar para mover",
                            key=f"select_original_{original_idx}",
                            value=st.session_state.selected_individual_files.get(f"original_{original_idx}", False)
                        )
                        if select_original:
                            st.session_state.selected_individual_files[f"original_{original_idx}"] = True
                            st.session_state.selected_individual_files[f"duplicate_{original_idx}"] = False
                        else:
                            st.session_state.selected_individual_files[f"original_{original_idx}"] = False
                    
                    # Arquivo Duplicado
                    with col2:
                        st.markdown("#### 📄 Arquivo Duplicado (Mais Recente)")
                        duplicate_path = row['duplicate_file']
                        relative_path_dup = os.path.relpath(duplicate_path, source_folder)
                        
                        st.write(f"**📍 Caminho Relativo:**")
                        st.code(relative_path_dup, language=None)
                        st.write(f"**📅 Data:** {row['duplicate_date']}")
                        st.write(f"**📂 Pasta:** `{os.path.dirname(relative_path_dup)}`")
                        
                        # Checkbox para selecionar duplicado
                        select_duplicate = st.checkbox(
                            "🚚 Selecionar para mover (Recomendado)",
                            key=f"select_duplicate_{original_idx}",
                            value=st.session_state.selected_individual_files.get(f"duplicate_{original_idx}", False)
                        )
                        if select_duplicate:
                            st.session_state.selected_individual_files[f"duplicate_{original_idx}"] = True
                            st.session_state.selected_individual_files[f"original_{original_idx}"] = False
                        else:
                            st.session_state.selected_individual_files[f"duplicate_{original_idx}"] = False
                    
                    # Botões de ação
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if st.button("📂 Abrir Pasta Original", key=f"open_orig_{original_idx}"):
                            os.startfile(os.path.dirname(original_path))
                    with col2:
                        if st.button("📂 Abrir Pasta Duplicado", key=f"open_dup_{original_idx}"):
                            os.startfile(os.path.dirname(duplicate_path))
                    with col3:
                        if st.button("🔄 Selecionar Duplicado", key=f"auto_select_{original_idx}"):
                            st.session_state.selected_individual_files[f"duplicate_{original_idx}"] = True
                            st.session_state.selected_individual_files[f"original_{original_idx}"] = False
                
                st.markdown("---")
            
            # Seção de movimentação
            st.subheader("🚚 Movimentação de Arquivos")
            
            # Coletar arquivos selecionados
            selected_files_list = []
            if 'selected_individual_files' in st.session_state:
                for key, selected in st.session_state.selected_individual_files.items():
                    if selected:
                        file_type, idx_str = key.split('_', 1)
                        idx = int(idx_str)
                        if idx < len(filtered_df):
                            row = filtered_df.iloc[idx]
                            if file_type == 'original':
                                file_path = row['original_file']
                            else:
                                file_path = row['duplicate_file']
                            
                            selected_files_list.append({
                                'path': file_path,
                                'name': row['file_name'],
                                'size': row['file_size'],
                                'type': file_type
                            })
            
            # Informações sobre seleções
            col1, col2 = st.columns(2)
            with col1:
                st.info(f"**📋 Arquivos selecionados:** {len(selected_files_list)}")
            with col2:
                st.info(f"**📁 Pasta destino:** `{source_folder}\\ArquivosDuplicados`")
            
            # Botão de mover
            button_text = f"🚚 Mover {len(selected_files_list)} Arquivo(s) Selecionado(s)" if selected_files_list else "🚚 Mover Arquivos Selecionados"
            button_disabled = len(selected_files_list) == 0
            
            if st.button(button_text, type="primary", disabled=button_disabled, help="Mover arquivos selecionados para pasta ArquivosDuplicados"):
                if selected_files_list:
                    delete_folder = create_delete_folder(source_folder)
                    
                    if delete_folder:
                        moved_count = 0
                        errors = []
                        
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        total_files = len(selected_files_list)
                        
                        for i, file_info in enumerate(selected_files_list):
                            file_to_move = file_info['path']
                            status_text.text(f"Movendo: {file_info['name']}")
                            
                            if os.path.exists(file_to_move):
                                if move_file_to_delete_folder(file_to_move, delete_folder):
                                    moved_count += 1
                                else:
                                    errors.append(f"Erro ao mover: {file_info['name']}")
                            else:
                                errors.append(f"Arquivo não encontrado: {file_info['name']}")
                            
                            progress_bar.progress((i + 1) / total_files)
                        
                        progress_bar.empty()
                        status_text.empty()
                        
                        if moved_count > 0:
                            st.success(f"🎉 {moved_count} arquivo(s) movido(s) com sucesso para:\n`{delete_folder}`")
                            
                            # Limpar seleções
                            if 'selected_individual_files' in st.session_state:
                                st.session_state.selected_individual_files.clear()
                            
                            if st.button("📂 Abrir Pasta de Destino", key="open_dest"):
                                os.startfile(delete_folder)
                        
                        if errors:
                            st.error("❌ Erros encontrados:")
                            for error in errors:
                                st.error(f"• {error}")
                    else:
                        st.error("❌ Não foi possível criar a pasta ArquivosDuplicados")
                else:
                    st.warning("⚠️ Nenhum arquivo selecionado para mover!")
            
            # Instruções
            if not selected_files_list:
                st.info("ℹ️ **Como usar:** Marque os checkboxes '🚚 Selecionar para mover' ao lado dos arquivos que deseja mover para a pasta ArquivosDuplicados.")
        else:
            st.info("ℹ️ Nenhum arquivo duplicado foi encontrado!")
        
        # Parar execução aqui - não continuar para a tela de análise
        return
    
    # APENAS se não há resultados, mostrar a tela de análise
    st.header("Análise de Arquivos Duplicados")
    
    if not folder_valid:
        st.info("👆 Selecione uma pasta na barra lateral para começar a análise")
    else:
        st.success(f"**Pasta Selecionada:** {source_folder}")
        if include_subdirs:
            st.info("🔍 **Modo:** Análise incluindo subpastas")
        else:
            st.info("🔍 **Modo:** Análise apenas da pasta principal")
    
    # Botão para iniciar análise
    if st.button("🔍 Iniciar Análise", disabled=not folder_valid, type="primary"):
        if folder_valid:
            comparator = FileComparator()
            
            with st.spinner("Analisando arquivos..."):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                status_text.text("Escaneando pasta e coletando informações dos arquivos...")
                all_files = []
                
                if include_subdirs:
                    for root, dirs, files in os.walk(source_folder):
                        for file in files:
                            file_path = os.path.join(root, file)
                            try:
                                file_stat = os.stat(file_path)
                                file_info = {
                                    'name': file,
                                    'path': file_path,
                                    'size': file_stat.st_size,
                                    'modified_time': file_stat.st_mtime,
                                    'hash': calculate_md5(file_path)
                                }
                                all_files.append(file_info)
                            except:
                                continue
                else:
                    for file in os.listdir(source_folder):
                        file_path = os.path.join(source_folder, file)
                        if os.path.isfile(file_path):
                            try:
                                file_stat = os.stat(file_path)
                                file_info = {
                                    'name': file,
                                    'path': file_path,
                                    'size': file_stat.st_size,
                                    'modified_time': file_stat.st_mtime,
                                    'hash': calculate_md5(file_path)
                                }
                                all_files.append(file_info)
                            except:
                                continue
                
                progress_bar.progress(50)
                
                status_text.text("Procurando arquivos duplicados...")
                duplicates = comparator.find_duplicates_in_folder(all_files)
                progress_bar.progress(75)
                
                status_text.text("Salvando resultados...")
                comparator.save_results(duplicates)
                progress_bar.progress(100)
                
                # Armazenar no session_state para persistir
                st.session_state.duplicates = duplicates
                st.session_state.all_files = all_files
                st.session_state.source_folder_analysis = source_folder
                
                status_text.text("Análise concluída!")
                time.sleep(1)
                progress_bar.empty()
                status_text.empty()
                
                # Recarregar para mostrar os resultados
                st.rerun()
    
    # Rodapé
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666;'>
            <p>Detector de Arquivos Duplicados v2.0 | Desenvolvido com ❤️ usando Streamlit</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()