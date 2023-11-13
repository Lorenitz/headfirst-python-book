def read_swim_data(filename):
    import statistics
    #Splitting the file name into variables
    FN = "Darius-13-100m-Fly.txt"
    FOLDER = "../swimdata/"

    swimer, age, distance, stroke = FN.removesuffix(".txt").split("-")

    # Retrieving data from file
    with open(FOLDER + FN) as file:
        lines = file.readlines()

    # Remember, that strip remove the break line
    times = lines[0].strip().split(",")  