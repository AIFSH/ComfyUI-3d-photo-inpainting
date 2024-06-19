import os,site
now_dir = os.path.dirname(os.path.abspath(__file__))
site_packages_roots = []
for path in site.getsitepackages():
    if "packages" in path:
        site_packages_roots.append(path)
if(site_packages_roots==[]):site_packages_roots=["%s/runtime/Lib/site-packages" % now_dir]

for site_packages_root in site_packages_roots:
    if os.path.exists(site_packages_root):
        try:
            with open("%s/3dphoto.pth" % (site_packages_root), "w") as f:
                f.write(
                    "%s\n%s/3dphoto\n"
                    % (now_dir,now_dir)
                )
            break
        except PermissionError:
            raise PermissionError

if os.path.isfile("%s/3dphoto.pth" % (site_packages_root)):
    print("!!!3dphoto path was added to " + "%s/3dphoto.pth" % (site_packages_root) 
    + "\n if meet No module named 'MiDas' error,please restart comfyui")


from huggingface_hub import snapshot_download

if not os.path.isfile(os.path.join(now_dir,"checkpoints","model-f46da743.pt")):
    snapshot_download(repo_id="camenduru/3d-photo-inpainting",local_dir=os.path.join(now_dir,"checkpoints"))
else:
    print("3d-photo-inpainting use cache models,make sure your 'checkpoints' complete")
    

from .nodes import TreeDNode,LoadImagePath,PreViewVideo

WEB_DIRECTORY = "./web"

# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "TreeDNode": TreeDNode,
    "LoadImagePath":LoadImagePath,
    "PreViewVideo":PreViewVideo
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "TreeDNode": "3d photo inpainting",
    "LoadImagePath":"LoadImagePath",
    "PreViewVideo":"PreViewVideo"
}
