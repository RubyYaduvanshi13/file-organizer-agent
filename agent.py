# agent.py - UPDATED with correct classifications
import os
import shutil
import json
from pathlib import Path
from collections import Counter

class FileOrganizerAgent:
    """
    AI Agent that organizes files intelligently
    """
    
    def __init__(self, workspace="agent_workspace"):
        self.workspace = Path(workspace)
        self.workspace.mkdir(exist_ok=True)
        self.memory_file = self.workspace / "memory.json"
        self.memory = self.load_memory()
        
        # COMPREHENSIVE RULES for file organization - FIXED!
        self.rules = {
            # Documents - INCLUDING .pages and .docx
            '.pdf': 'Documents',
            '.doc': 'Documents',
            '.docx': 'Documents',  # ← This is correct
            '.pages': 'Documents',  # ← ADD THIS! Mac Pages documents
            '.txt': 'Documents',
            '.rtf': 'Documents',
            '.odt': 'Documents',
            '.tex': 'Documents',
            '.md': 'Documents',
            '.wpd': 'Documents',
            
            # Images
            '.jpg': 'Images',
            '.jpeg': 'Images',
            '.png': 'Images',
            '.gif': 'Images',
            '.bmp': 'Images',
            '.svg': 'Images',
            '.webp': 'Images',
            '.ico': 'Images',
            '.tiff': 'Images',
            '.psd': 'Images',
            '.ai': 'Images',
            
            # Presentations - INCLUDING .pptx
            '.ppt': 'Presentations',    # ← ADD THIS
            '.pptx': 'Presentations',    # ← This is correct
            '.key': 'Presentations',
            '.odp': 'Presentations',
            
            # Spreadsheets
            '.xls': 'Spreadsheets',
            '.xlsx': 'Spreadsheets',
            '.csv': 'Spreadsheets',
            '.ods': 'Spreadsheets',
            '.numbers': 'Spreadsheets',
            
            # Code
            '.py': 'Code',
            '.js': 'Code',
            '.html': 'Code',
            '.css': 'Code',
            '.java': 'Code',
            '.cpp': 'Code',
            '.c': 'Code',
            '.h': 'Code',
            '.php': 'Code',
            '.rb': 'Code',
            '.go': 'Code',
            '.rs': 'Code',
            '.swift': 'Code',
            '.kt': 'Code',
            '.ts': 'Code',
            '.jsx': 'Code',
            '.tsx': 'Code',
            '.json': 'Data',
            '.xml': 'Data',
            '.yaml': 'Data',
            '.yml': 'Data',
            '.toml': 'Data',
            '.ini': 'Config',
            '.cfg': 'Config',
            '.conf': 'Config',
            '.sh': 'Scripts',
            '.bash': 'Scripts',
            '.zsh': 'Scripts',
            '.ps1': 'Scripts',
            
            # Archives
            '.zip': 'Archives',
            '.rar': 'Archives',
            '.7z': 'Archives',
            '.tar': 'Archives',
            '.gz': 'Archives',
            '.bz2': 'Archives',
            '.xz': 'Archives',
            
            # Audio
            '.mp3': 'Audio',
            '.wav': 'Audio',
            '.flac': 'Audio',
            '.aac': 'Audio',
            '.ogg': 'Audio',
            '.m4a': 'Audio',
            
            # Video
            '.mp4': 'Video',
            '.avi': 'Video',
            '.mkv': 'Video',
            '.mov': 'Video',
            '.wmv': 'Video',
            '.flv': 'Video',
            '.webm': 'Video',
            
            # System files - HIDE or IGNORE
            '.ds_store': 'System',  # Mac system file
            '.DS_Store': 'System',  # ← ADD THIS
            'desktop.ini': 'System',
            '.git': 'System',
            '.gitignore': 'System',
        }
        
        print("🤖 Agent initialized with comprehensive rules")
        print(f"📁 Workspace: {self.workspace}")
        print(f"📋 Loaded {len(self.rules)} file type rules")
    
    def load_memory(self):
        """Load agent's memory from file"""
        if self.memory_file.exists():
            try:
                return json.loads(self.memory_file.read_text())
            except:
                return {'learned': {}, 'history': []}
        return {'learned': {}, 'history': []}
    
    def save_memory(self):
        """Save agent's memory to file"""
        self.memory_file.write_text(json.dumps(self.memory, indent=2))
    
    def ensure_folder_exists(self, folder_name):
        """Create folder if it doesn't exist"""
        if folder_name == 'System':
            return None  # Don't create System folder, just ignore
        folder_path = self.workspace / folder_name
        folder_path.mkdir(exist_ok=True)
        return folder_path
    
    def decide_where_to_put(self, file_path):
        """
        AI makes decision about file location
        """
        filename = file_path.name.lower()
        ext = Path(file_path).suffix.lower()
        
        # Skip system files
        if filename in ['.ds_store', '.ds_store', 'desktop.ini'] or ext in ['.ds_store']:
            return None  # Signal to delete/ignore
        
        # 1. Check if learned from past experience
        if ext in self.memory['learned']:
            print(f"   🧠 Using learned rule: {ext} → {self.memory['learned'][ext]}")
            return self.memory['learned'][ext]
        
        # 2. Check default rules
        if ext in self.rules:
            return self.rules[ext]
        
        # 3. Unknown extension - default to Other
        return 'Other'
    
    def organize(self, specific_files=None):
        """
        Main agent function - organizes files into folders
        """
        print(f"\n🔍 Scanning for files to organize...")
        
        # Get files to organize
        if specific_files:
            files = [Path(f) for f in specific_files if Path(f).exists()]
            print(f"📁 Processing {len(files)} specified files")
        else:
            # Only get files in root workspace (not in subfolders)
            files = [f for f in self.workspace.iterdir() 
                    if f.is_file() and f.name != "memory.json"]
            print(f"📁 Found {len(files)} files in workspace root")
        
        if len(files) == 0:
            print("✅ No files need organizing!")
            return []
        
        results = []
        print("\n🤖 Agent organizing files...")
        
        for file_path in files:
            try:
                # AGENT DECIDES where to put it
                folder = self.decide_where_to_put(file_path)
                
                # If folder is None, it's a system file - delete it
                if folder is None:
                    os.remove(file_path)
                    print(f"   🗑️ Removed system file: {file_path.name}")
                    continue
                
                # AGENT CREATES folder if needed
                dest_folder = self.ensure_folder_exists(folder)
                if dest_folder is None:
                    continue
                
                # AGENT MOVES the file
                dest = dest_folder / file_path.name
                
                # Handle duplicate filenames
                if dest.exists():
                    base = dest.stem
                    suffix = dest.suffix
                    counter = 1
                    while dest.exists():
                        new_name = f"{base}_{counter}{suffix}"
                        dest = dest_folder / new_name
                        counter += 1
                
                shutil.move(str(file_path), str(dest))
                
                # Record the action
                result = {
                    'file': file_path.name,
                    'from': 'root',
                    'to': folder,
                    'status': 'success'
                }
                results.append(result)
                self.memory['history'].append(result)
                print(f"   ✅ {file_path.name} → {folder}/")
                
            except Exception as e:
                results.append({
                    'file': file_path.name,
                    'error': str(e),
                    'status': 'failed'
                })
                print(f"   ❌ Failed to organize {file_path.name}: {e}")
        
        # AGENT LEARNS from this experience
        self.learn_from_history()
        
        # Save memory
        self.save_memory()
        
        # Summary
        success_count = len([r for r in results if r['status'] == 'success'])
        print(f"\n📊 Organization complete! {success_count} files organized")
        
        return results
    
    def learn_from_history(self):
        """
        Agent learns patterns from successful organizations
        """
        for action in self.memory['history']:
            if action['status'] == 'success':
                file_name = action['file']
                folder = action['to']
                ext = Path(file_name).suffix.lower()
                
                # Learn extension patterns
                if ext and folder and ext not in self.memory['learned']:
                    # Don't overwrite existing learned rules
                    if ext not in self.memory['learned']:
                        self.memory['learned'][ext] = folder
                        print(f"   🧠 Learned: {ext} files go to {folder}")
    
    def get_status(self):
        """Get current agent status"""
        # Count all files
        all_files = list(self.workspace.rglob('*'))
        file_count = len([f for f in all_files if f.is_file() and f.name != "memory.json"])
        
        # Count folders
        folders = [f for f in self.workspace.iterdir() if f.is_dir()]
        
        # Count files in root (unorganized)
        root_files = [f for f in self.workspace.iterdir() 
                     if f.is_file() and f.name != "memory.json"]
        
        return {
            'workspace': str(self.workspace),
            'total_files': file_count,
            'unorganized_files': len(root_files),
            'folders_created': len(folders),
            'folder_names': [str(f.name) for f in folders],
            'learned_patterns': len(self.memory['learned']),
            'memory_size': len(self.memory['history'])
        }


# For testing directly
if __name__ == "__main__":
    # Create agent
    agent = FileOrganizerAgent()
    
    # Show status
    print("\n📊 Initial Status:", agent.get_status())
    
    # Run organization
    results = agent.organize()
    
    # Show final status
    print("\n📊 Final Status:", agent.get_status())
