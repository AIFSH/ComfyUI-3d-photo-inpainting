import os
import sys
import folder_paths
import yaml
input_dir = folder_paths.get_input_directory()
now_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = folder_paths.get_output_directory()
ckpt_dir = os.path.join(now_dir,"checkpoints")
threed_dir = os.path.join(output_dir,"3D_Photo")
depth_dir = os.path.join(threed_dir,"depth")
mesh_dir = os.path.join(threed_dir,"mesh")
video_dir = os.path.join(threed_dir,"video")

class TreeDNode:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "img_path": ("IMAGEPATH",),
                "fps": ("INT",{
                    "default": 40
                }),
                "num_frames": ("INT",{
                    "default": 240
                }),
                "x_shift":("FLOAT",{
                    "default": 0.00,
                    "round": 0.001,
                    "display": "number"
                }),
                "y_shift":("FLOAT",{
                    "default": 0.00,
                    "round": 0.001,
                    "display": "number"
                }),
                "z_shift":("FLOAT",{
                    "default": -0.05,
                    "round": 0.001,
                    "display": "number"
                }),
                "traj_type":(['double-straight-line','circle'],{
                    "default": 'double-straight-line'
                }),
                "video_postfix":(['dolly-zoom-in', 'zoom-in', 'circle', 'swing'],{
                    "default": 'dolly-zoom-in'
                }),
                "offscreen_rendering":("BOOLEAN",{
                    "default": True
                })
            }
        }
    RETURN_TYPES = ("VIDEO",)
    #RETURN_NAMES = ("image_output_name",)

    FUNCTION = "render"

    #OUTPUT_NODE = False

    CATEGORY = "AIFSH_3d-photo-inpainting"

    def render(self,img_path,fps,num_frames,x_shift,y_shift,z_shift,traj_type,video_postfix,offscreen_rendering):
        python_exec = sys.executable or "python"
        infer_py = os.path.join(now_dir,"3dphoto","main.py")
        default_yaml_path = os.path.join(now_dir,"3dphoto","argument.yml")
        with open(default_yaml_path, 'r', encoding="utf-8") as f:
            yaml_data = yaml.load(f.read(),Loader=yaml.SafeLoader)
        yaml_data['depth_edge_model_ckpt'] = os.path.join(ckpt_dir,"edge-model.pth")
        yaml_data['depth_feat_model_ckpt'] = os.path.join(ckpt_dir,"depth-model.pth")
        yaml_data['rgb_feat_model_ckpt'] = os.path.join(ckpt_dir,"color-model.pth")
        yaml_data['MiDaS_model_ckpt'] = os.path.join(ckpt_dir,"model.pt")
        yaml_data['use_boostmonodepth'] = False
        yaml_data['fps'] = fps
        yaml_data['num_frames'] = num_frames
        yaml_data['x_shift_range'] = [x_shift]
        yaml_data['y_shift_range'] = [y_shift]
        yaml_data['z_shift_range'] = [z_shift]
        yaml_data['traj_types'] = [traj_type]
        yaml_data['video_postfix'] = [video_postfix]
        yaml_data['specific'] = img_path
        yaml_data['src_folder'] = input_dir
        yaml_data['depth_folder'] = depth_dir
        yaml_data['mesh_folder'] = mesh_dir
        yaml_data['video_folder'] = video_dir
        yaml_data['img_format'] = img_path[-4:]
        yaml_data['offscreen_rendering'] = offscreen_rendering

        tmp_yaml_path = os.path.join(now_dir,'tmp.yaml')
        with open(tmp_yaml_path,'w', encoding="utf-8") as f:
            yaml.dump(data=yaml_data,stream=f,Dumper=yaml.Dumper)
        
        cmd = f"""{python_exec} {infer_py} --config "{tmp_yaml_path}" """
        os.system(cmd)
        outfile = ""
        os.remove(tmp_yaml_path)
        return (outfile,)

class LoadImagePath:
    @classmethod
    def INPUT_TYPES(s):
        
        files = [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]
        return {"required":
                    {"image": (sorted(files), {"image_upload": True})},
                }

    CATEGORY = "AIFSH_Hallo"

    RETURN_TYPES = ("IMAGEPATH",)
    FUNCTION = "load_image"
    def load_image(self, image):
        image_path = folder_paths.get_annotated_filepath(image)
        return (image_path,)
    
class PreViewVideo:
    @classmethod
    def INPUT_TYPES(s):
        return {"required":{
            "video":("VIDEO",),
        }}
    
    CATEGORY = "AIFSH_Hallo"
    DESCRIPTION = "hello world!"

    RETURN_TYPES = ()

    OUTPUT_NODE = True

    FUNCTION = "load_video"

    def load_video(self, video):
        video_name = os.path.basename(video)
        video_path_name = os.path.basename(os.path.dirname(video))
        return {"ui":{"video":[video_name,video_path_name]}}
