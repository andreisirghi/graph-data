import datetime
from uuid import uuid4
from faker import Factory
import random

fake = Factory.create('en_US')

CHARACTERISTIC_TYPES = (
    'country',
    'city',
    'university',
    'faculty',
    'street',
    'date_of_birth',
    'year_enrolled',
    'year_graduated',
    'hobby',
)


def get_student_csv_header():
    return ('idno',
            'name',
            'description',
            'phone',
            'country',
            'city',
            'address',
            'university',
            'faculty',
            'date_of_birth',
            'date_enrolled',
            )


def get_student_characteristic_csv_header():
    return ('idno',
            'type',
            'value',
            )


def get_student_as_csv_row(student: dict):
    return (student['idno'],
            student['name'],
            student['description'],
            student['phone'],
            student['country'],
            student['city'],
            student['address'],
            student['university'],
            student['faculty'],
            student['date_of_birth'],
            student['date_enrolled'],)


def get_student_characteristic_rows(student: dict):
    result = []
    for characteristic in student['characteristics']:
        result.append((
            student['idno'],
            characteristic['type'],
            characteristic['value'],
        ))
    return result


def generate_student():
    date_of_birth = fake.date_time_between(start_date='-45y', end_date='-22y')
    street_name = fake.street_name()
    building_number = fake.building_number()

    date_enrolled = random_date_enrolled(date_of_birth)
    student = {
        'idno': str(uuid4()),
        'name': fake.name(),
        'description': fake.text(),
        'phone': fake.phone_number(),
        'country': fake.country(),
        'city': fake.city(),
        'address': '{} {}'.format(building_number, street_name),
        'university': random_university(),
        'faculty': random_faculty(),
        'date_of_birth': date_of_birth.date().isoformat(),
        'date_enrolled': date_enrolled.date().isoformat(),
    }
    # characteristics
    student_characteristics = [
        ('country', student['country']),
        ('city', student['city']),
        ('university', student['university']),
        ('faculty', student['faculty']),
        ('street', street_name),
        ('date_of_birth', student['date_of_birth']),
        ('year_enrolled', str(date_enrolled.year)),
    ]
    # add graduation year
    current_year = datetime.datetime.now().year
    if current_year - date_enrolled.year > 4:
        student_characteristics.append(
            ('year_graduated', str(random.choice(
                range(date_enrolled.year, current_year - 4)))))
    # add some hobbies
    hobbies = random.choice(range(1, 4))
    while hobbies >= 0:
        hobbies -= 1
        student_characteristics.append(('hobby', random_hobby()))
    student['characteristics'] = [{'type': key, 'value': value}
                                  for key, value in student_characteristics]
    return student


def random_date_enrolled(dob):
    date = datetime.datetime.now()
    date = date.replace(day=random.choice(range(1, 28)))
    date = date.replace(month=random.choice(range(6, 10)))
    date = date.replace(year=random.choice(range(dob.year + 19, date.year)))
    return date


def pick_friends(student_ids):
    if len(student_ids) < 50:
        return []
    else:
        friends = []
        friends_nr = random.choice(range(5, 20))
        while friends_nr:
            friends.append(random.choice(student_ids))
            friends_nr -= 1
        return friends


def random_university():
    # Randomly return one university name from the following list
    universities = [
        "Harvard University",
        "Stanford University",
        "Massachusetts Institute of Technology (MIT)",
        "University of California-Berkeley",
        "University of Cambridge",
        "Princeton University",
        "California Institute of Technology",
        "Columbia University",
        "University of Chicago",
        "University of Oxford",
        "Yale University",
        "University of California, Los Angeles",
        "Cornell University",
        "University of California, San Diego",
        "University of Washington",
        "University of Pennsylvania",
        "The Johns Hopkins University",
        "University of California, San Francisco",
        "Swiss Federal Institute of Technology Zurich",
        "University College London",
        "The University of Tokyo",
        "The Imperial College of Science, Technology and Medicine",
        "University of Michigan-Ann Arbor",
        "University of Toronto",
        "University of Wisconsin - Madison",
        "Kyoto University",
        "New York University",
        "Northwestern University",
        "University of Illinois at Urbana-Champaign",
        "University of Minnesota, Twin Cities",
        "Duke University",
        "Washington University in St. Louis",
        "Rockefeller University",
        "University of Colorado at Boulder",
        "Pierre and Marie Curie University - Paris 6",
        "University of North Carolina at Chapel Hill",
        "University of British Columbia",
        "The University of Manchester",
        "The University of Texas at Austin",
        "University of Copenhagen",
        "University of California, Santa Barbara",
        "University of Paris Sud (Paris 11)",
        "University of Maryland, College Park",
        "The University of Melbourne",
        "The University of Edinburgh",
        "The University of Texas Southwestern Medical Center at Dallas",
        "Karolinska Institute",
        "University of California, Irvine",
        "Heidelberg University",
        "University of Munich",
        "University of Southern California",
        "Rutgers, The State University of New Jersey - New Brunswick",
        "Technical University Munich",
        "Vanderbilt University",
        "University of California, Davis",
        "University of Zurich",
        "Utrecht University",
        "Pennsylvania State University - University Park",
        "King's College London",
        "Purdue University - West Lafayette",
        "Uppsala University",
        "Carnegie Mellon University",
        "University of Bristol",
        "The Ohio State University - Columbus",
        "University of Pittsburgh-Pittsburgh Campus",
        "University of Geneva",
        "Ecole Normale Superieure - Paris",
        "McGill University",
        "University of Oslo",
        "Ghent University",
        "The Hebrew University of Jerusalem",
        "Boston University",
        "University of Helsinki",
        "Aarhus University",
        "Brown University",
        "The Australian National University",
        "Leiden University",
        "Osaka University",
        "Stockholm University",
        "Technion-Israel Institute of Technology",
        "University of Florida",
        "Rice University",
        "University of Groningen",
        "Moscow State University",
        "The University of Queensland",
        "University of Arizona",
        "University of Utah",
        "Arizona State University",
        "The University of Western Australia",
        "McMaster University",
        "University of Basel",
        "University of Rochester",
        "University of California, Santa Cruz",
        "University of Bonn",
        "University of Strasbourg",
        "KU Leuven",
        "Swiss Federal Institute of Technology Lausanne",
        "Texas A & M University",
        "Georgia Institute of Technology",
        "VU University Amsterdam",
        "Aix Marseille University",
        "Baylor College of Medicine",
        "Cardiff University",
        "Case Western Reserve University",
        "Catholic University of Louvain",
        "Emory University",
        "Hokkaido University",
        "Indiana University Bloomington",
        "Joseph Fourier University (Grenoble 1)",
        "London School of Economics and Political Science",
        "Lund University",
        "Mayo Medical School",
        "Michigan State University",
        "Monash University",
        "Nagoya University",
        "National Taiwan University",
        "National University of Singapore",
        "Peking University",
        "Radboud University Nijmegen",
        "Seoul National University",
        "Shanghai Jiao Tong University",
        "Technical University of Denmark",
        "The University of Glasgow",
        "The University of New South Wales",
        "The University of Sheffield",
        "The University of Texas M. D. Anderson Cancer Center",
        "Tohoku University",
        "Tsinghua University",
        "Tufts University",
        "University Libre Bruxelles",
        "University of Alberta",
        "University of Amsterdam",
        "University of Birmingham",
        "University of California, Riverside",
        "University of Frankfurt",
        "University of Freiburg",
        "University of Goettingen",
        "University of Leeds",
        "University of Liverpool",
        "University of Massachusetts Amherst",
        "University of Massachusetts Medical School - Worcester",
        "University of Montreal",
        "University of Nottingham",
        "University of Sao Paulo",
        "University of Southampton",
        "University of Sydney",
        "University of Virginia",
        "University of Wageningen",
        "University Paris Diderot - Paris 7",
        "Weizmann Institute of Science",
        "Erasmus University",
        "Fudan University",
        "George Mason University",
        "Icahn School of Medicine at Mount Sinai",
        "Iowa State University",
        "King Abdulaziz University",
        "King Saud University",
        "Kyushu University",
        "Nanyang Technological University",
        "North Carolina State University - Raleigh",
        "Oregon Health and Science University",
        "Oregon State University",
        "Tel Aviv University",
        "The Chinese University of Hong Kong",
        "The University of Adelaide",
        "The University of Calgary",
        "The University of Georgia",
        "The University of Hong Kong",
        "Tokyo Institute of Technology",
        "Trinity College Dublin",
        "University of Barcelona",
        "University of Bern",
        "University of Bologna",
        "University of Buenos Aires",
        "University of Delaware",
        "University of East Anglia",
        "University of Gothenburg",
        "University of Hamburg",
        "University of Hawaii at Manoa",
        "University of Illinois at Chicago",
        "University of Iowa",
        "University of Kiel",
        "University of Koeln",
        "University of Lausanne",
        "University of Miami",
        "University of Milan",
        "University of Muenster",
        "University of Padua",
        "University of Paris Descartes (Paris 5)",
        "University of Pisa",
        "University of Roma - La Sapienza",
        "University of Science and Technology of China",
        "University of Sussex",
        "University of Tuebingen",
        "University of Turin",
        "University of Vienna",
        "University of Warwick",
        "University of Wuerzburg",
        "Virginia Commonwealth University",
        "Zhejiang University",
        "Autonomous University of Barcelona",
        "Autonomous University of Madrid",
        "Beijing Normal University",
        "Charles University in Prague",
        "City University of Hong Kong",
        "Claude Bernard University Lyon 1",
        "Colorado State University",
        "Dalhousie University",
        "Dartmouth College",
        "Delft University of Technology",
        "Durham University",
        "Ecole Normale Superieure - Lyon",
        "Florida State University",
        "Harbin Institute of Technology",
        "Huazhong University of Science and Technology",
        "Karlsruhe Institute of Technology (KIT)",
        "Kobe University",
        "Korea Advanced Institute of Science and Technology",
        "Korea University",
        "Laval University",
        "Louisiana State University - Baton Rouge",
        "Maastricht University",
        "Macquarie University",
        "Medical University of Vienna",
        "Nanjing University",
        "National Autonomous University of Mexico",
        "National Cheng Kung University",
        "National Tsing Hua University",
        "Newcastle University",
        "Northeastern University",
        "Norwegian University of Science and Technology - NTNU",
        "Paul Sabatier University (Toulouse 3)",
        "Polytechnic Institute of Milan",
        "Queen Mary, University of London",
        "Queen's University",
        "Rensselaer Polytechnic Institute",
        "Royal Institute of Technology",
        "RWTH Aachen University",
        "Simon Fraser University",
        "State University of New York at Buffalo",
        "Stony Brook University",
        "Sun Yat-sen University",
        "Sungkyunkwan University",
        "Swedish University of Agricultural Sciences",
        "The George Washington University",
        "The Hong Kong University of Science and Technology",
        "The University of Alabama at Birmingham",
        "The University of Auckland",
        "The University of Dundee",
        "The University of New Mexico - Albuquerque",
        "The University of Texas Health Science Center at Houston",
        "TU Dresden",
        "Umea University",
        "University College Dublin",
        "University of Aberdeen",
        "University of Bergen",
        "University of Bochum",
        "University of Bordeaux",
        "University of Cape Town",
        "University of Cincinnati",
        "University of Erlangen-Nuremberg",
        "University of Exeter",
        "University of Florence",
        "University of Guelph",
        "University of Houston",
        "University of Innsbruck",
        "University of Kansas",
        "University of Kentucky",
        "University of Leicester",
        "University of Leipzig",
        "University of Liege",
        "University of Lisbon",
        "University of Lorraine",
        "University of Mainz",
        "University of Marburg",
        "University of Maryland, Baltimore",
        "University of Missouri - Columbia",
        "University of Montpellier 2",
        "University of Nebraska - Lincoln",
        "University of Notre Dame",
        "University of Oregon",
        "University of Otago",
        "University of Ottawa",
        "University of South Carolina - Columbia",
        "University of South Florida",
        "University of St Andrews",
        "University of Stuttgart",
        "University of Tennessee - Knoxville",
        "University of the Witwatersrand",
        "University of Tsukuba",
        "University of Valencia",
        "University of Victoria",
        "University of Waterloo",
        "University of York",
        "Virginia Polytechnic Institute and State University",
        "Washington State University",
        "Western University (The University of Western Ontario)",
        "Xian Jiao Tong University",
        "Yeshiva University",
        "Yonsei University",
        "Beihang University",
        "Brandeis University",
        "Brigham Young University",
        "Central South University",
        "Chalmers University of Technology",
        "Chiba University",
        "China Agricultural University",
        "City University of New York City College",
        "Complutense University of Madrid",
        "Curtin University",
        "Dalian University of Technology",
        "Drexel University",
        "Ecole Polytechnique",
        "Eindhoven University of Technology",
        "Eotvos Lorand University",
        "ESPCI ParisTech",
        "Federal University of Minas Gerais",
        "Federal University of Rio de Janeiro",
        "Flinders University",
        "Georgetown University",
        "Griffith University",
        "Hannover Medical School",
        "Hanyang University",
        "Hiroshima University",
        "Indian Institute of Science",
        "Indiana University-Purdue University at Indianapolis",
        "Jagiellonian University",
        "James Cook University",
        "Jilin University",
        "Keio University",
        "Kyung Hee University",
        "Lancaster University",
        "Lanzhou University",
        "Linkoping University",
        "London School of Hygiene & Tropical Medicine",
        "Nankai University",
        "National and Kapodistrian University of Athens",
        "National Chiao Tung University",
        "Pohang University of Science and Technology",
        "Polytechnic University of Valencia",
        "Queen's University Belfast",
        "Saint Petersburg State University",
        "San Diego State University",
        "Scuola Normale Superiore - Pisa",
        "Shandong University",
        "Sichuan University",
        "South China University of Technology",
        "Southeast University",
        "SUNY at Albany",
        "Swinburne University of Technology",
        "Technical University of Berlin",
        "Temple University",
        "The Hong Kong Polytechnic University",
        "The University of Montana - Missoula",
        "The University of Reading",
        "The University of Texas at Dallas",
        "The University of Texas Health Science Center at San Antonio",
        "Thomas Jefferson University",
        "Tokyo Medical and Dental University",
        "Tongji University",
        "Tulane University",
        "UNESP",
        "University of Antwerp",
        "University of Belgrade",
        "University of Campinas",
        "University of Central Florida",
        "University of Colorado at Denver",
        "University of Connecticut",
        "University of Duesseldorf",
        "University of Duisburg-Essen",
        "University of Giessen",
        "University of Granada",
        "University of Halle-Wittenberg",
        "University of Konstanz",
        "University of Malaya",
        "University of Manitoba",
        "University of Milan - Bicocca",
        "University of Naples Federico II",
        "University of Newcastle",
        "University of Oulu",
        "University of Paris Dauphine (Paris 9)",
        "University of Pompeu Fabra",
        "University of Porto",
        "University of Rhode Island",
        "University of Roma - Tor Vergata",
        "University of Saskatchewan",
        "University of Southern Denmark",
        "University of Tasmania",
        "University of Technology, Sydney",
        "University of Tehran",
        "University of Turku",
        "University of Twente",
        "University of Ulm",
        "University of Vermont",
        "University of Warsaw",
        "University of Wollongong",
        "Vrije University Brussel",
        "Wake Forest University",
        "Wayne State University",
        "Xiamen University",
        "Aalborg University",
        "Aalto University",
        "Aristotle University of Thessaloniki",
        "Auburn University",
        "Bar-Ilan University",
        "Ben-Gurion University of the Negev",
        "Bielefeld University",
        "Boston College",
        "Brunel University",
        "Cairo University",
        "Capital University of Medical Sciences",
        "Carleton University",
        "Catholic University of Chile",
        "Catholic University of Korea",
        "Catholic University of the Sacred Heart",
        "Chang Gung University",
        "Clemson University",
        "Deakin University",
        "East China University of Science and Technology",
        "Ewha Womans University",
        "Federal University of Rio Grande do Sul",
        "Istanbul University",
        "Kanazawa University",
        "Kansas State University",
        "Kent State University",
        "King Abdullah University of Science and Technology",
        "King Fahd University of Petroleum & Minerals",
        "Medical University of Graz",
        "Medical University of South Carolina",
        "MINES ParisTech",
        "Nanjing Medical University",
        "National Sun Yat-Sen University",
        "National Yang Ming University",
        "Okayama University",
        "Oklahoma State University",
        "Osaka City University",
        "Peking Union Medical College",
        "Polytechnic University of Catalonia",
        "Rush University",
        "Saint Louis University",
        "Soochow University",
        "State University of New York Health Science Center at Brooklyn",
        "Stellenbosch University",
        "Stockholm School of Economics",
        "Syracuse University",
        "Technical University Darmstadt",
        "Technical University of Braunschweig",
        "The Open University",
        "The University of Texas Medical Branch at Galveston",
        "Tianjin University",
        "Tilburg University",
        "Tokyo University of Science",
        "University College Cork",
        "University of Alaska - Fairbanks",
        "University of Arkansas at Fayetteville",
        "University of Arkansas at Little Rock",
        "University of Auvergne",
        "University of Bath",
        "University of Bayreuth",
        "University of Bremen",
        "University of Cagliari",
        "University of Canterbury",
        "University of Chile",
        "University of Coimbra",
        "University of Eastern Finland",
        "University of Essex",
        "University of Ferrara",
        "University of Genova",
        "University of Graz",
        "University of Hannover",
        "University of Jena",
        "University of KwaZulu-Natal",
        "University of Ljubljana",
        "University of Maryland, Baltimore County",
        "University of New Hampshire - Durham",
        "University of Nice Sophia Antipolis",
        "University of Oklahoma - Norman",
        "University of Palermo",
        "University of Parma",
        "University of Pavia",
        "University of Perugia",
        "University of Quebec",
        "University of Regensburg",
        "University of Rennes 1",
        "University of Rostock",
        "University of Santiago Compostela",
        "University of Science, Malaysia",
        "University of Surrey",
        "University of Szeged",
        "University of Tennessee Health Science Center",
        "University of the Basque Country",
        "University of Trieste",
        "University of Wyoming",
        "University of Zaragoza",
        "Utah State University",
        "Victoria University of Wellington",
        "Vienna University of Technology",
        "Waseda University",
        "Wuhan University",
        "York University",
    ]
    return random.choice(universities)


def random_faculty():
    # Randomly return one faculty name from the following list
    faculties = [
        "Accountancy",
        "Allied Health and Communicative Disorders",
        "Anthropology",
        "Art and Design",
        "Biological Sciences ",
        "Chemistry and Biochemistry",
        "Communication",
        "Computer Science",
        "Counseling, Adult and Higher Education",
        "Economics",
        "Educational Technology, Research and Assessment",
        "Electrical Engineering",
        "English",
        "Environmental Studies",
        "Family, Consumer and Nutrition Sciences",
        "Finance",
        "Foreign Languages and Literatures",
        "Geography",
        "Geology and Environmental Geosciences",
        "History",
        "Industrial and Systems Engineering",
        "Kinesiology and Physical Education",
        "Leadership, Educational Psychology and Foundations",
        "Literacy and Elementary Education",
        "Management",
        "Marketing",
        "Mathematical Sciences",
        "Mechanical Engineering",
        "Military Science",
        "Music",
        "Non-Governmental Organization Leadership & Development",
        "Nursing and Health Studies",
        "Operations Management and Information Systems",
        "Philosophy",
        "Physics",
        "Political Science",
        "Psychology",
        "Public and Global Affairs",
        "Public Administration",
        "Sociology",
        "Special and Early Education",
        "Statistics",
        "Technology",
        "Theatre and Dance",
    ]
    return random.choice(faculties)


def random_hobby():
    # Randomly return one hobby name from the following list
    hobbies = [
        "3D printing",
        "Amateur radio",
        "Acting",
        "Baton twirling",
        "Board games",
        "Book restoration",
        "Cabaret",
        "Calligraphy",
        "Candle making",
        "Computer programming",
        "Coffee roasting",
        "Cooking",
        "Coloring",
        "Cosplaying",
        "Couponing",
        "Creative writing",
        "Crocheting",
        "Crossword puzzles",
        "Cryptography",
        "Dance",
        "Digital arts",
        "Drama",
        "Drawing",
        "Do it yourself",
        "Electronics",
        "Embroidery",
        "Fashion",
        "Flower arranging",
        "Foreign language learning",
        "Gaming (tabletop games and role-playing games)",
        "Gambling",
        "Genealogy",
        "Glassblowing",
        "Gunsmithing",
        "Homebrewing",
        "Ice skating",
        "Jewelry making",
        "Jigsaw puzzles",
        "Juggling",
        "Knapping",
        "Knitting",
        "Kabaddi",
        "Knife making",
        "Kombucha Brewing",
        "Lacemaking",
        "Lapidary",
        "Lego building",
        "Lockpicking",
        "Lucid dreaming",
        "Machining",
        "Macrame",
        "Metalworking",
        "Magic",
        "Model building",
        "Listening to music",
        "Origami",
        "Painting",
        "Playing musical instruments",
        "Pet",
        "Poi",
        "Pottery",
        "Puzzles",
        "Quilting",
        "Reading",
        "Scrapbooking",
        "Sculpting",
        "Sewing",
        "Singing",
        "Sketching",
        "Soapmaking",
        "Stand-up comedy",
        "Table tennis",
        "Video gaming",
        "Watching movies",
        "Web surfing",
        "Whittling",
        "Wood carving",
        "Woodworking",
        "Worldbuilding",
        "Writing",
        "Yoga",
        "Yo-yoing",
        "Air sports",
        "Archery",
        "Astronomy",
        "Backpacking",
        "BASE jumping",
        "Baseball",
        "Basketball",
        "Beekeeping",
        "Bird watching",
        "Blacksmithing",
        "Board sports",
        "Bodybuilding",
        "Brazilian jiu-jitsu",
        "Community",
        "Cycling",
        "Camping",
        "Dowsing",
        "Driving",
        "Fishing ",
        "Flag Football",
        "Flying",
        "Flying disc",
        "Foraging",
        "Gardening",
        "Geocaching",
        "Ghost hunting",
        "Graffiti",
        "Handball",
        "Hiking",
        "Hooping",
        "Horseback riding",
        "Hunting",
        "Inline skating",
        "Jogging",
        "Kayaking",
        "Kite flying",
        "Kitesurfing",
        "LARPing",
        "Letterboxing",
        "Metal detecting",
        "Motor sports",
        "Mountain biking",
        "Mountaineering",
        "Mushroom hunting/Mycology",
        "Netball",
        "Nordic skating",
        "Orienteering",
        "Paintball",
        "Parkour",
        "Photography",
        "Polo",
        "Rafting",
        "Rappelling",
        "Rock climbing",
        "Roller skating",
        "Rugby",
        "Running",
        "Sailing",
        "Sand art",
        "Scouting",
        "Scuba diving",
        "Sculling or Rowing",
        "Topiary",
        "Shooting",
        "Shopping",
        "Skateboarding",
        "Skiing",
        "Skimboarding",
        "Skydiving",
        "Slacklining",
        "Snowboarding",
        "Stone skipping",
        "Surfing",
        "Swimming",
        "Taekwondo",
        "Tai chi",
        "Urban exploration",
        "Vacation",
        "Vehicle restoration",
        "Walking",
        "Water sports",
    ]
    return random.choice(hobbies)
