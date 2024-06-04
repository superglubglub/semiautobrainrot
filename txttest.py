
# %%
# importing editor from movie py 
from moviepy.editor import *

# text 
text = "Example Subtitle Text"
  
# creating a text clip 
# having font arial-bold 
# with font size = 70 
# and color = green 

clip = TextClip(text,
                                 fontsize=70,
                                 color="white",
                                 font="Simply-Rounded-Bold",
                                 method='caption',
                                 align="North",
                                 stroke_color="black",
                                 stroke_width=10
                                )
clip2 = TextClip(text,
                                 fontsize=70,
                                 color="white",
                                 font="Simply-Rounded-Bold",
                                 method='caption',
                                 align="North"
                                )


composite = CompositeVideoClip([clip, clip2])
print(TextClip.list("font"))

# showing  clip  
composite.save_frame("text_example.png")
