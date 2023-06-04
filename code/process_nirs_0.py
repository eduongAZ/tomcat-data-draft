from pipeline import process_experiment

if __name__ == "__main__":
    path_to_task = '/Users/ericduong/Documents/ToMCAT/tomcat-data-draft/data/raw/tasks'
    path_to_physio = '/Users/ericduong/Documents/ToMCAT/tomcat-data-draft/data/separated/physio_data'
    path_to_experiment_info = '/Users/ericduong/Documents/ToMCAT/tomcat-data-draft/data/organized/info'
    physio_type = 'nirs'
    output_path = '/Users/ericduong/Documents/ToMCAT/tomcat-data-draft/data/processed'

    experiments = [
        "exp_2022_10_14_10"
    ]

    process_experiment(
        path_to_task,
        path_to_physio,
        path_to_experiment_info,
        physio_type,
        experiments,
        output_path
    )
