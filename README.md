# MIE_1075
Project Name:
Shopping Assistant Robot:


Project Proposal
 
Group 10 

Zicheng Wang 1005730130
Sourabh Prasad 100727217
Xingjian Li 1011563096
Hankun Wang 1011796344

Project Statement:
These robots should be used in malls (like Walmart).
Tasks:
Task Command and Execution: The system will take the customer's voice command and process it with LLM (Mike and Lester).
Processing information from the supermarket's database, checking availability and locating the item (Mike and Lester).
Path planning: Plan and execute a collision-free path to approach the identified object, avoiding obstacles and navigating within the supermarket layout. This can be done by either MPC or reinforcement learning.
Automatic grabbing: Using reinforcement learning to train the robot to grab items of different sizes and orientations. 
Image processing: To identify the item and determine the posture in which the goods should be grabbed. 
If fetching the item for the user, perform facial detection to correctly return it to the user. (Samuel)
AI usage: 
Reinforcement learning for grabbing items.
Image processing for identifying items and object detection. 
Image segmentation to distinguish a single item from the other items on the shelf.
Large Language Model for processing the voice command of customers.
Facial detection for returning the item to the correct user.
Assumption：
Sensors - Stereo/depth camera for object detection. LiDar for path planning and collision avoidance.
To ensure efficient item retrieval, users are requested and assumed to remain at their original location while the robot fetches the requested item.
	




Background:
Reinforcement Learning and Automatic Grabbing:
[1, 2, 5] Perform advanced image processing and automatic grabbing techniques to help tasks 4 and 5. 
Large Language Model:
BERT (Bidirectional Encoder Representations from Transformers) and GPT (Generative Pretrained Transformer) are both based on the Transformer architecture[3, 4]. BERT has an encoder-based architecture, which is useful in understanding sentences. We intend to use the model to process user instructions. GPT is a decoder-based large language model, which generates the next tokens by its previous word. We plan to use GPT in response generation. 
Image Segmentation:
[6] Image segmentation is partitioning an image into individual segments (groups of pixels) related to the same class.
Facial detection:
[7] This book details facial detection. So, it will help with task 6.

Proposed Design Methodology：
Voice Command Processing with LLM: Utilize a pre-trained LLM to process customer’s voice commands. Integration with a speech to text engine for capturing voice input. Demonstrate how the robot understands and processes voice commands, translating them into database queries for item retrieval. 
Grabbing Object: Use reinforcement learning to train the robots to manipulate its arm to grab items of different sizes, weights and shapes. Using image processing to assist in identifying the item’s orientation and determine the optimal grasp.
Image Processing and Object Segmentation: Image processing techniques are used to segment objects on the shelves and identify the target item for grabbing. Stereo/depth cameras will aid in determining the item's position and orientation.
Facial detection: Utilize a facial recognition algorithm (e.g., CNN) to ensure that the robot returns the item to the correct user.

We plan to demo command Processing with LLM, path planning and facial detection. Due to 3D modeling and long reinforcement learning training time, we cannot guarantee to demonstrate the entire project.





Reference:

[1] G. Ma et al., “A machine vision based sealing rings automatic grabbing and putting system,” in 2016 IEEE 14th International Conference on Industrial Informatics (INDIN), IEEE, 2016, pp. 202–206. doi: 10.1109/INDIN.2016.7819159.

[2] L.-H. Juang, “Humanoid robot fetching objects using monocular vision unit,” Multimedia tools and applications, vol. 82, no. 5, pp. 6747–6767, 2023, doi: 10.1007/s11042-022-13602-8.

[3] G. Yenduri et al., “Generative Pre-trained transformer: A comprehensive review on enabling technologies, potential applications, emerging challenges, and future directions,” arXiv.org, https://arxiv.org/abs/2305.10435 (accessed Oct. 2, 2024). 

[4] J. Devlin, M.-W. Chang, K. Lee, and K. Toutanova, “Bert: Pre-training of deep bidirectional Transformers for language understanding,” arXiv.org, https://arxiv.org/abs/1810.04805 (accessed Oct. 2, 2024). 

[5] Robotic grasping using deep reinforcement learning, https://arxiv.org/pdf/2007.04499 (accessed Oct. 2, 2024). 

[6] Segformer: Simple and efficient design for semantic ..., https://arxiv.org/pdf/2105.15203 (accessed Oct. 2, 2024). 

[7] Michal. Kawulok, Emre. Celebi, and Bogdan. Smolka, Eds., Advances in Face Detection and Facial Image Analysis, 1st ed. 2016. Cham: Springer International Publishing, 2016. doi: 10.1007/978-3-319-25958-1.
