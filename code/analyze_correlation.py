from models import regression, NIRS_CHANNELS, EEG_CHANNELS

physio_task_data_location = "/tomcat/data/derived/drafts/draft_2023_06_05_11"

nirs_ping_pong_cooperative_target_file = "ping_pong_cooperative_physio_task.csv"
nirs_ping_pong_cooperative_physio_task_dir = f"{physio_task_data_location}/nirs"
nirs_ping_pong_cooperative_image_output_dir = "./code_outputs/ping_pong_cooperative/nirs"

regression(
    nirs_ping_pong_cooperative_physio_task_dir,
    nirs_ping_pong_cooperative_target_file,
    "score_left",
    NIRS_CHANNELS,
    nirs_ping_pong_cooperative_image_output_dir
)

eeg_ping_pong_cooperative_target_file = "ping_pong_cooperative_physio_task.csv"
eeg_ping_pong_cooperative_physio_task_dir = f"{physio_task_data_location}/eeg"
eeg_ping_pong_cooperative_image_output_dir = "./code_outputs/ping_pong_cooperative/eeg"

regression(
    eeg_ping_pong_cooperative_physio_task_dir,
    eeg_ping_pong_cooperative_target_file,
    "score_left",
    EEG_CHANNELS,
    eeg_ping_pong_cooperative_image_output_dir
)

nirs_minecraft_saturn_a_target_file = "minecraft_saturn_a_physio_task.csv"
nirs_minecraft_saturn_a_physio_task_dir = f"{physio_task_data_location}/nirs"
nirs_minecraft_saturn_a_image_output_dir = "./code_outputs/minecraft_saturn_a/nirs"

regression(
    nirs_minecraft_saturn_a_physio_task_dir,
    nirs_minecraft_saturn_a_target_file,
    "score",
    NIRS_CHANNELS,
    nirs_minecraft_saturn_a_image_output_dir
)

eeg_minecraft_saturn_a_target_file = "minecraft_saturn_a_physio_task.csv"
eeg_minecraft_saturn_a_physio_task_dir = f"{physio_task_data_location}/eeg"
eeg_minecraft_saturn_a_image_output_dir = "./code_outputs/minecraft_saturn_a/eeg"

regression(
    eeg_minecraft_saturn_a_physio_task_dir,
    eeg_minecraft_saturn_a_target_file,
    "score",
    EEG_CHANNELS,
    eeg_minecraft_saturn_a_image_output_dir
)

nirs_minecraft_saturn_b_target_file = "minecraft_saturn_b_physio_task.csv"
nirs_minecraft_saturn_b_physio_task_dir = f"{physio_task_data_location}/nirs"
nirs_minecraft_saturn_b_image_output_dir = "./code_outputs/minecraft_saturn_b/nirs"

regression(
    nirs_minecraft_saturn_b_physio_task_dir,
    nirs_minecraft_saturn_b_target_file,
    "score",
    NIRS_CHANNELS,
    nirs_minecraft_saturn_b_image_output_dir
)

eeg_minecraft_saturn_b_target_file = "minecraft_saturn_b_physio_task.csv"
eeg_minecraft_saturn_b_physio_task_dir = f"{physio_task_data_location}/eeg"
eeg_minecraft_saturn_b_image_output_dir = "./code_outputs/minecraft_saturn_b/eeg"

regression(
    eeg_minecraft_saturn_b_physio_task_dir,
    eeg_minecraft_saturn_b_target_file,
    "score",
    EEG_CHANNELS,
    eeg_minecraft_saturn_b_image_output_dir
)
