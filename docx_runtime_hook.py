import sys
import os
import shutil
from pathlib import Path

def fix_docx_templates():
    if not getattr(sys, 'frozen', False):
        return

    # In a frozen environment (PyInstaller)
    if sys.platform == 'darwin':
        # macOS BUNDLE
        # Executable is in Contents/MacOS/md2gbt9704
        # Resources are in Contents/Resources/
        # Libraries are in Contents/Frameworks/
        app_bundle_path = Path(sys.executable).parent.parent.parent
        resources_docx = app_bundle_path / "Contents" / "Resources" / "docx"
        frameworks_docx = app_bundle_path / "Contents" / "Frameworks" / "docx"
        
        print(f"[HOOK] macOS bundle detected", file=sys.stderr)
        print(f"[HOOK] resources_docx: {resources_docx}", file=sys.stderr)
        print(f"[HOOK] frameworks_docx: {frameworks_docx}", file=sys.stderr)

        if resources_docx.exists():
            try:
                # If frameworks_docx is a symlink, delete it
                if frameworks_docx.is_symlink():
                    print(f"[HOOK] Deleting symlink {frameworks_docx}", file=sys.stderr)
                    frameworks_docx.unlink()
                
                # If it's already a directory, it's fine
                if not frameworks_docx.exists():
                    print(f"[HOOK] Creating directory {frameworks_docx}", file=sys.stderr)
                    os.makedirs(frameworks_docx, exist_ok=True)
                
                # Create the parts directory so that parts/../templates works
                parts_dir = frameworks_docx / "parts"
                os.makedirs(parts_dir, exist_ok=True)
                print(f"[HOOK] Created parts directory {parts_dir}", file=sys.stderr)
                
                # Link or copy templates from Resources to Frameworks/docx/templates
                templates_src = resources_docx / "templates"
                templates_dst = frameworks_docx / "templates"
                
                if templates_src.exists() and not templates_dst.exists():
                    try:
                        # Try to symlink first (faster and cleaner)
                        # Use relative path for portability
                        os.symlink("../../Resources/docx/templates", templates_dst)
                        print(f"[HOOK] Created symlink for templates: {templates_dst} -> Resources", file=sys.stderr)
                    except Exception as e:
                        # Fallback to copy
                        shutil.copytree(templates_src, templates_dst)
                        print(f"[HOOK] Copied templates: {templates_dst}", file=sys.stderr)
                elif templates_dst.exists():
                    print(f"[HOOK] Templates destination already exists: {templates_dst}", file=sys.stderr)
            except Exception as e:
                print(f"[HOOK] Failed to fix docx structure: {e}", file=sys.stderr)
        else:
            print(f"[HOOK] Resources docx NOT found at {resources_docx}", file=sys.stderr)
    
    elif sys.platform == 'win32':
        # Windows onedir/onefile
        meipass = getattr(sys, '_MEIPASS', os.path.dirname(sys.executable))
        docx_resources = os.path.join(meipass, 'docx')
        
        print(f"[HOOK] Windows environment detected", file=sys.stderr)
        print(f"[HOOK] docx_resources: {docx_resources}", file=sys.stderr)

        if os.path.exists(docx_resources):
            try:
                import docx
                docx_module_dir = os.path.dirname(docx.__file__)
                templates_src = os.path.join(docx_resources, 'templates')
                templates_dest = os.path.join(docx_module_dir, 'templates')
                parts_dir = os.path.join(docx_module_dir, 'parts')

                # Create parts directory for path resolution
                if not os.path.exists(parts_dir):
                    os.makedirs(parts_dir, exist_ok=True)
                
                if os.path.exists(templates_src) and not os.path.exists(templates_dest):
                    shutil.copytree(templates_src, templates_dest)
                    print(f"[HOOK] Successfully copied templates to {templates_dest}", file=sys.stderr)
            except Exception as e:
                print(f"[HOOK] Failed to copy templates on Windows: {e}", file=sys.stderr)

try:
    fix_docx_templates()
except Exception as e:
    print(f"[HOOK] Critical error in docx hook: {e}", file=sys.stderr)
