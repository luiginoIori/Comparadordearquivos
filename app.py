import streamlit as st
import os
import hashlib
from pathlib import Path
import pandas as pd
from datetime import datetime
import json
from typing import Dict, List, Tuple
import time
import tkinter as tk
from tkinter import filedialog

class FileComparator:
    def __init__(self):
        self.duplicate_files = []
        self.processed_files = 0
        self.total_files = 0
    
    def get_file_hash(self, file_path: str) -> str:
        """Calcula o hash MD5 do arquivo para comparação de conteúdo"""
        hash_md5 = hashlib.md5()
        try:
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception:
            return None
    
    def get_file_info(self, file_path: str) -> Dict:
        """Coleta informações detalhadas do arquivo"""
        try:
            stat = os.stat(file_path)
            return {
                'path': file_path,
                'name': os.path.basename(file_path),
                'size': stat.st_size,
                'modified_time': stat.st_mtime,
                'created_time': stat.st_ctime,
                'hash': self.get_file_hash(file_path)
            }
        except Exception as e:
            st.error(f"Erro ao processar arquivo {file_path}: {str(e)}")
            return None
    
    def scan_directory(self, directory: str) -> List[Dict]:
        """Escaneia diretório recursivamente e coleta informações de todos os arquivos"""
        files_info = []
        
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                file_info = self.get_file_info(file_path)
                if file_info and file_info['hash']:
                    files_info.append(file_info)
                    self.processed_files += 1
        
        return files_info
    
    def find_duplicates(self, source_files: List[Dict], compare_files: List[Dict]) -> List[Dict]:
        """Encontra arquivos duplicados baseado em nome, tamanho, data e hash"""
        duplicates = []
        
        # Criar índice dos arquivos de comparação para busca eficiente
        compare_index = {}
        for file_info in compare_files:
            key = (file_info['name'], file_info['size'], file_info['modified_time'])
            if key not in compare_index:
                compare_index[key] = []
            compare_index[key].append(file_info)
        
        # Comparar arquivos da pasta fonte
        for source_file in source_files:
            key = (source_file['name'], source_file['size'], source_file['modified_time'])
            
            if key in compare_index:
                for compare_file in compare_index[key]:
                    # Verificar se o hash também coincide (conteúdo idêntico)
                    if source_file['hash'] == compare_file['hash']:
                        duplicates.append({
                            'source_file': source_file['path'],
                            'duplicate_file': compare_file['path'],
                            'file_name': source_file['name'],
                            'file_size': source_file['size'],
                            'modified_date': datetime.fromtimestamp(source_file['modified_time']).strftime('%Y-%m-%d %H:%M:%S'),
                            'hash': source_file['hash']
                        })
        
        return duplicates
    
    def save_results(self, duplicates: List[Dict], filename: str = "duplicados_encontrados.json"):
        """Salva os resultados em arquivo JSON"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(duplicates, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            st.error(f"Erro ao salvar arquivo: {str(e)}")
            return False

def format_file_size(size_bytes: int) -> str:
    """Formata o tamanho do arquivo em formato legível"""
    if size_bytes == 0:
        return "0 B"
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    return f"{size_bytes:.2f} {size_names[i]}"

def select_folder(title: str) -> str:
    """Abre um diálogo para seleção de pasta"""
    try:
        # Configurar tkinter para não mostrar janela principal
        root = tk.Tk()
        root.withdraw()
        root.wm_attributes('-topmost', 1)
        
        # Abrir diálogo de seleção de pasta
        folder_path = filedialog.askdirectory(
            title=title,
            mustexist=True
        )
        
        # Fechar tkinter
        root.destroy()
        
        return folder_path if folder_path else ""
    except Exception as e:
        st.error(f"Erro ao abrir seletor de pasta: {str(e)}")
        st.info("💡 Como alternativa, você pode digitar o caminho da pasta manualmente no campo abaixo.")
        return ""

def get_common_folders():
    """Retorna uma lista de pastas comuns do Windows"""
    common_folders = []
    try:
        # Pasta do usuário
        user_folder = os.path.expanduser("~")
        common_folders.append(("🏠 Pasta do Usuário", user_folder))
        
        # Desktop
        desktop = os.path.join(user_folder, "Desktop")
        if os.path.exists(desktop):
            common_folders.append(("🖥️ Área de Trabalho", desktop))
        
        # Documents
        documents = os.path.join(user_folder, "Documents")
        if os.path.exists(documents):
            common_folders.append(("📁 Documentos", documents))
        
        # Downloads
        downloads = os.path.join(user_folder, "Downloads")
        if os.path.exists(downloads):
            common_folders.append(("⬇️ Downloads", downloads))
        
        # Pictures
        pictures = os.path.join(user_folder, "Pictures")
        if os.path.exists(pictures):
            common_folders.append(("🖼️ Imagens", pictures))
        
        # Drives disponíveis
        for drive in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            drive_path = f"{drive}:\\"
            if os.path.exists(drive_path):
                common_folders.append((f"💾 Drive {drive}:", drive_path))
    
    except Exception:
        pass
    
    return common_folders

def main():
    st.set_page_config(
        page_title="Comparador de Arquivos Duplicados",
        page_icon="🔍",
        layout="wide"
    )
    
    st.title("🔍 Comparador de Arquivos Duplicados")
    st.markdown("---")
    
    # Sidebar para configurações
    st.sidebar.header("Configurações")
    
    # Seleção de pastas
    st.sidebar.subheader("Seleção de Diretórios")
    
    # Inicializar session state para as pastas
    if 'source_folder' not in st.session_state:
        st.session_state.source_folder = ""
    if 'compare_folder' not in st.session_state:
        st.session_state.compare_folder = ""
    if 'show_manual_input' not in st.session_state:
        st.session_state.show_manual_input = False
    
    # Pasta de Origem
    st.sidebar.write("**🗂️ Pasta de Origem:**")
    
    # Botões de ação para pasta de origem
    col1, col2, col3 = st.sidebar.columns([2, 1, 1])
    with col1:
        if st.button("📁 Navegar", key="select_source", help="Abrir seletor de pasta"):
            selected_folder = select_folder("Selecione a Pasta de Origem")
            if selected_folder:
                st.session_state.source_folder = selected_folder
                st.rerun()
    
    with col2:
        if st.button("⌨️", key="manual_source", help="Digitar caminho manualmente"):
            st.session_state.show_manual_input = not st.session_state.show_manual_input
            st.rerun()
    
    with col3:
        if st.button("🗑️", key="clear_source", help="Limpar seleção"):
            st.session_state.source_folder = ""
            st.rerun()
    
    # Exibir pasta selecionada ou campo manual
    if st.session_state.show_manual_input:
        manual_source = st.sidebar.text_input(
            "Digite o caminho da pasta de origem:",
            value=st.session_state.source_folder,
            placeholder="Ex: C:\\Meus Documentos",
            key="manual_source_input"
        )
        if manual_source and os.path.exists(manual_source):
            st.session_state.source_folder = manual_source
            st.sidebar.success("✅ Pasta válida!")
        elif manual_source:
            st.sidebar.error("❌ Pasta não encontrada!")
    else:
        if st.session_state.source_folder:
            st.sidebar.success(f"✅ **Selecionada:** {st.session_state.source_folder}")
        else:
            st.sidebar.info("ℹ️ Nenhuma pasta selecionada")
    
    # Pastas comuns para origem
    common_folders = get_common_folders()
    if common_folders:
        st.sidebar.write("**🔗 Pastas Comuns:**")
        for name, path in common_folders[:4]:  # Mostrar apenas as 4 primeiras
            if st.sidebar.button(name, key=f"common_source_{path}", help=f"Selecionar: {path}"):
                st.session_state.source_folder = path
                st.rerun()
    
    st.sidebar.markdown("---")
    
    # Pasta para Comparação
    st.sidebar.write("**🔍 Pasta para Comparação:**")
    
    # Botões de ação para pasta de comparação
    col1, col2, col3 = st.sidebar.columns([2, 1, 1])
    with col1:
        if st.button("📁 Navegar", key="select_compare", help="Abrir seletor de pasta"):
            selected_folder = select_folder("Selecione a Pasta para Comparação")
            if selected_folder:
                st.session_state.compare_folder = selected_folder
                st.rerun()
    
    with col2:
        if st.button("⌨️", key="manual_compare", help="Digitar caminho manualmente"):
            st.session_state.show_manual_input = not st.session_state.show_manual_input
            st.rerun()
    
    with col3:
        if st.button("🗑️", key="clear_compare", help="Limpar seleção"):
            st.session_state.compare_folder = ""
            st.rerun()
    
    # Exibir pasta selecionada ou campo manual para comparação
    if st.session_state.show_manual_input:
        manual_compare = st.sidebar.text_input(
            "Digite o caminho da pasta de comparação:",
            value=st.session_state.compare_folder,
            placeholder="Ex: D:\\Backup",
            key="manual_compare_input"
        )
        if manual_compare and os.path.exists(manual_compare):
            st.session_state.compare_folder = manual_compare
            st.sidebar.success("✅ Pasta válida!")
        elif manual_compare:
            st.sidebar.error("❌ Pasta não encontrada!")
    else:
        if st.session_state.compare_folder:
            st.sidebar.success(f"✅ **Selecionada:** {st.session_state.compare_folder}")
        else:
            st.sidebar.info("ℹ️ Nenhuma pasta selecionada")
    
    # Pastas comuns para comparação
    if common_folders:
        st.sidebar.write("**� Pastas Comuns:**")
        for name, path in common_folders[:4]:  # Mostrar apenas as 4 primeiras
            if st.sidebar.button(name, key=f"common_compare_{path}", help=f"Selecionar: {path}"):
                st.session_state.compare_folder = path
                st.rerun()
    
    # Usar as pastas do session state
    source_folder = st.session_state.source_folder
    compare_folder = st.session_state.compare_folder
    
    # Validação das pastas
    folders_valid = False
    if source_folder and compare_folder:
        if os.path.exists(source_folder) and os.path.exists(compare_folder):
            folders_valid = True
            st.sidebar.success("✅ Pastas válidas")
        else:
            st.sidebar.error("❌ Uma ou ambas as pastas não existem")
    
    # Área principal
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("Análise de Arquivos Duplicados")
        
        if not folders_valid:
            st.info("👆 Selecione as pastas na barra lateral para começar a análise")
        else:
            st.success(f"**Pasta de Origem:** {source_folder}")
            st.success(f"**Pasta de Comparação:** {compare_folder}")
    
    with col2:
        st.header("Estatísticas")
        stats_placeholder = st.empty()
    
    # Botão para iniciar análise
    if st.button("🔍 Iniciar Análise", disabled=not folders_valid, type="primary"):
        if folders_valid:
            comparator = FileComparator()
            
            with st.spinner("Analisando arquivos..."):
                # Progress bar
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Escanear pasta de origem
                status_text.text("Escaneando pasta de origem...")
                source_files = comparator.scan_directory(source_folder)
                progress_bar.progress(25)
                
                # Escanear pasta de comparação
                status_text.text("Escaneando pasta de comparação...")
                compare_files = comparator.scan_directory(compare_folder)
                progress_bar.progress(50)
                
                # Encontrar duplicatas
                status_text.text("Procurando arquivos duplicados...")
                duplicates = comparator.find_duplicates(source_files, compare_files)
                progress_bar.progress(75)
                
                # Salvar resultados
                status_text.text("Salvando resultados...")
                comparator.save_results(duplicates)
                progress_bar.progress(100)
                
                status_text.text("Análise concluída!")
                time.sleep(1)
                progress_bar.empty()
                status_text.empty()
            
            # Exibir resultados
            st.header("📊 Resultados da Análise")
            
            # Estatísticas
            with stats_placeholder.container():
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Arquivos na Origem", len(source_files))
                with col2:
                    st.metric("Arquivos na Comparação", len(compare_files))
                with col3:
                    st.metric("Duplicados Encontrados", len(duplicates))
                with col4:
                    if duplicates:
                        total_size = sum(dup['file_size'] for dup in duplicates)
                        st.metric("Espaço Duplicado", format_file_size(total_size))
            
            if duplicates:
                st.success(f"✅ Encontrados {len(duplicates)} arquivos duplicados!")
                
                # Criar DataFrame para exibição
                df = pd.DataFrame(duplicates)
                df['file_size_formatted'] = df['file_size'].apply(format_file_size)
                
                # Exibir tabela
                st.subheader("📋 Lista de Arquivos Duplicados")
                
                # Filtros
                col1, col2 = st.columns(2)
                with col1:
                    name_filter = st.text_input("Filtrar por nome:", placeholder="Digite parte do nome do arquivo")
                with col2:
                    size_filter = st.selectbox(
                        "Filtrar por tamanho:",
                        ["Todos", "< 1 MB", "1-10 MB", "10-100 MB", "> 100 MB"]
                    )
                
                # Aplicar filtros
                filtered_df = df.copy()
                
                if name_filter:
                    filtered_df = filtered_df[filtered_df['file_name'].str.contains(name_filter, case=False, na=False)]
                
                if size_filter != "Todos":
                    if size_filter == "< 1 MB":
                        filtered_df = filtered_df[filtered_df['file_size'] < 1024*1024]
                    elif size_filter == "1-10 MB":
                        filtered_df = filtered_df[(filtered_df['file_size'] >= 1024*1024) & (filtered_df['file_size'] < 10*1024*1024)]
                    elif size_filter == "10-100 MB":
                        filtered_df = filtered_df[(filtered_df['file_size'] >= 10*1024*1024) & (filtered_df['file_size'] < 100*1024*1024)]
                    elif size_filter == "> 100 MB":
                        filtered_df = filtered_df[filtered_df['file_size'] >= 100*1024*1024]
                
                # Exibir tabela filtrada
                display_df = filtered_df[['file_name', 'file_size_formatted', 'modified_date', 'source_file', 'duplicate_file']].copy()
                display_df.columns = ['Nome do Arquivo', 'Tamanho', 'Data Modificação', 'Arquivo Original', 'Arquivo Duplicado']
                
                st.dataframe(
                    display_df,
                    use_container_width=True,
                    hide_index=True
                )
                
                # Opções de download
                st.subheader("💾 Exportar Resultados")
                col1, col2 = st.columns(2)
                
                with col1:
                    # Download JSON
                    json_data = json.dumps(duplicates, indent=2, ensure_ascii=False)
                    st.download_button(
                        label="📄 Baixar JSON",
                        data=json_data,
                        file_name=f"duplicados_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json"
                    )
                
                with col2:
                    # Download CSV
                    csv_data = display_df.to_csv(index=False, encoding='utf-8-sig')
                    st.download_button(
                        label="📊 Baixar CSV",
                        data=csv_data,
                        file_name=f"duplicados_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
                
                # Seção para exclusão de arquivos
                st.subheader("🗑️ Gerenciar Arquivos Duplicados")
                st.warning("⚠️ **Atenção:** A exclusão de arquivos é permanente e não pode ser desfeita!")
                
                selected_indices = st.multiselect(
                    "Selecione os arquivos duplicados para exclusão:",
                    options=range(len(filtered_df)),
                    format_func=lambda x: f"{filtered_df.iloc[x]['file_name']} ({format_file_size(filtered_df.iloc[x]['file_size'])})"
                )
                
                if selected_indices:
                    if st.button("🗑️ Excluir Arquivos Selecionados", type="secondary"):
                        deleted_count = 0
                        errors = []
                        
                        for idx in selected_indices:
                            duplicate_path = filtered_df.iloc[idx]['duplicate_file']
                            try:
                                os.remove(duplicate_path)
                                deleted_count += 1
                                st.success(f"✅ Excluído: {os.path.basename(duplicate_path)}")
                            except Exception as e:
                                errors.append(f"❌ Erro ao excluir {os.path.basename(duplicate_path)}: {str(e)}")
                        
                        if deleted_count > 0:
                            st.success(f"🎉 {deleted_count} arquivo(s) excluído(s) com sucesso!")
                        
                        for error in errors:
                            st.error(error)
                
            else:
                st.info("ℹ️ Nenhum arquivo duplicado foi encontrado!")
    
    # Rodapé
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666;'>
            <p>Comparador de Arquivos Duplicados v1.0 | Desenvolvido com ❤️ usando Streamlit</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()