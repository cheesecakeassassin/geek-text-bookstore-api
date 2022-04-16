from app.db import Session, Base, engine
from app.models import Book, Author, Review, User

# Drop and rebuild tables
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

db = Session()

# Insert users
db.add_all([
    User(name="Fernando",
         username="fernandosantamarta",
         email="fsanta076@fbi.gov",
         home_address="123 SW 56 Street",
         password="test123"),

    User(name="Sasha",
         username="thedinoinstitute",
         email="sashascannell@mit.edu",
         home_address="354 NW 44 Street",
         password="test123"),

    User(name="Thamare",
         username="Thamare1",
         email="thamaresaintlouis@aol.com",
         home_address="789 SW 22 Street",
         password="test123"),

    User(name="Karim",
         username="AbdulJabaar",
         email="karimthedream@bellsouth.net",
         home_address="555 NW 10 Street",
         password="test123"),

    User(name="Sebastian",
         username="cheesecakeassassin",
         email="seabass96@yahoo.com",
         home_address="965 SW 30 Street",
         password="test123"),

    User(name="Camilo",
         username="puesyo",
         email="puesyonose@gmail.com",
         home_address="523 NW 16 Street",
         password="test123")
])

db.commit()

# Insert reviews
db.add_all([
    Review(rating="5",
           comment="Excellent book! Enjoyed it! I hope there is a sequel!",
           user_username="puesyo",
           book_id=1),

    Review(rating="3",
           comment="Good book, but could have used more cowbell...",
           user_username="thedinoinstitute",
           book_id=1),

    Review(rating="3",
           comment="The book was decent if I am quite honest.",
           user_username="Thamare1",
           book_id=1),

    Review(rating="4",
           comment="Great book, Frankenstein's monster was so scary!",
           user_username="cheesecakeassassin",
           book_id=2),

    Review(rating="5",
           comment="Amazing book! Enjoyed it! Mary Shelley is a beast!",
           user_username="AbdulJabaar",
           book_id=2),

    Review(rating="3",
           comment="Good book overall, but the ending sucked!",
           user_username="fernandosantamarta",
           book_id=2)
])

db.commit()

# Insert books
db.add_all([
    Book(title="Little Women",
         author="Louisa May Alcott",
         isbn=9781593081089,
         publisher="Barnes & Noble",
         genre="Literature",
         price=8.95,
         year_published=2009,
         description="Generations of readers young and old, male and female, have fallen in love with Little Women",
         sold_copies=3000),

    Book(title="Frankenstein",
         author="Mary Shelley",
         isbn=9780143131847,
         publisher="Penguin Publishing Group",
         genre="Literature",
         price=8.95,
         year_published=2018,
         description="Mary Shelley's seminal novel of the scientist whose creation becomes a monster.",
         sold_copies=250),

    Book(title="The Picture of Dorian Gray",
         author="Oscar Wilde",
         isbn=9781593080259,
         publisher="Barnes & Noble",
         genre="Literature",
         price=7.95,
         year_published=2003,
         description="Oscar Wilde brings his enormous gifts for astute social observation and sparkling prose to The Picture of Dorian Gray",
         sold_copies=3100),

    Book(title="Wuthering Heights",
         author="Emily Bronte",
         isbn=9780141439556,
         publisher="Penguin Publishing Group",
         genre="Fiction",
         price=7.95,
         year_published=2002,
         description="Wuthering Heights is a wild, passionate story of the intense and almost demonic love.",
         sold_copies=1000),

    Book(title="Treasure Island",
         author="Robert Louis Stevenson",
         isbn=9781593082475,
         publisher="Barnes & Noble",
         genre="Adventure",
         price=7.95,
         year_published=2005,
         description="The most popular pirate story ever written in English, featuring one of literature's most beloved.",
         sold_copies=800),

    Book(title="Fahrenheit 451: A Novel",
         author="Ray Bradbury",
         isbn=9781451673319,
         publisher="Simon & Schuster",
         genre="Literature",
         price=13.99,
         description="Guy Montag is a fireman. His job is to destroy the most illegal of commodities, the printed book.",
         year_published=2012,
         sold_copies=1500),

    Book(title="Alice's Adventures in Wonderland & Through The Looking Glass",
         author="Lewis Carroll",
         isbn=9781533653697,
         publisher="CreateSpace Publishing",
         genre="Childrens",
         price=12.0,
         year_published=2016,
         description="The young Alice is bored in a too conventional world. But here goes a White Rabbit.",
         sold_copies=900),

    Book(title="Peter Pan",
         author="J.M.Barrie",
         isbn=9780805072457,
         publisher="Henry Holt and Co.",
         genre="Childrens",
         price=7.99,
         year_published=2003,
         description="Peter Pan, the mischievous boy who refuses to grow up.",
         sold_copies=2300),

    Book(title="A Wrinkle in Time",
         author="Madeleine L'Engle",
         isbn=9780312367541,
         publisher="Square Fish",
         genre="Childrens",
         price=6.99,
         year_published=2007,
         description="Out of this wild night, a strange visitor comes to the Murry house and beckons Meg.",
         sold_copies=1350),

    Book(title="The Wizard of Oz",
         author="L. Frank Baum",
         isbn=9780141321028,
         publisher="Penguin Publishing Group",
         genre="Childrens",
         price=7.99,
         year_published=2008,
         description="Dorothy thinks she is lost forever when a terrifying tornado crashes through Kansas.",
         sold_copies=3600),

    Book(title="The Secret of the Old Clock (Nancy Drew Mystery Stories #1)",
         author="Carolyn Keene",
         isbn=9780448095011,
         publisher="Applewood Books",
         genre="Childrens",
         price=8.99,
         year_published=1991,
         description="Nancy, unaided, seeks to find a missing will.",
         sold_copies=750),

    Book(title="In Cold Blood",
         author="Truman Capote",
         isbn=9780679745587,
         publisher="Knopf Doubleday Publishing Group",
         genre="True), Crime",
         price=14.95,
         year_published=1994,
         description="On November 15, 1959, in the small town of Holcomb, Kansas, four members of the Clutter family were savagely murdered.",
         sold_copies=1200),

    Book(title="The Devil in the White City",
         author="Erik Larson",
         isbn=9780609608449,
         publisher="Crown Publishers",
         genre="True), Crime",
         price=14.95,
         year_published=1994,
         description="Two men, each handsome and unusually adept at his chosen work, embodied an element of the great dynamic.",
         sold_copies=4000),

    Book(title="Helter Skelter: The True), Story of the Manson Murders",
         author="Vincent Bugliosi, Curt Gentry",
         isbn=9780393322231,
         publisher="W.W. Norton ny",
         genre="True), Crime",
         price=14.49,
         year_published=2001,
         description="In the summer of 1969, in Los Angeles, a series of brutal, seemingly random murders captured headlines across America.",
         sold_copies=2700),

    Book(title="Zodiac: The Shocking True)",
         author="Robert Graysmith",
         isbn=9780425212189,
         publisher="Penguin Publishing Group",
         genre="True), Crime",
         price=8.99,
         year_published=2007,
         description="A sexual sadist, the Zodiac killer took pleasure in torture and murder. His first victims were a teenage couple.",
         sold_copies=3200),

    Book(title="The Road to Jonestown: Jim Jones and Peoples Temple",
         author="Jeff Guinn",
         isbn=9781476763835,
         publisher="Simon & Schuster",
         genre="True), Crime",
         price=15.99,
         year_published=2018,
         description="In the 1950s, a young Indianapolis minister named Jim Jones preached a curious blend of the gospel and Marxism.",
         sold_copies=1800),

    Book(title="The Talented Mr. Ripley",
         author="Patricia Highsmith",
         isbn=9780393332148,
         publisher="W.W. Norton ny",
         genre="Thriller",
         price=12.95,
         year_published=2008,
         description="Since his debut in 1955, Tom Ripley has evolved into the ultimate bad boy sociopath.",
         sold_copies=1500),

    Book(title="Murder on the Orient Express",
         author="Agatha Christie",
         isbn=9780007119318,
         publisher="HarperCollins",
         genre="Thriller",
         price=8.99,
         year_published=2007,
         description="Just after midnight, a snowdrift stops the Orient Express in its tracks as it travels through the mountainous Balkans.",
         sold_copies=900),

    Book(title="The Shining",
         author="Stephen King",
         isbn=9780450040184,
         publisher="New English Library",
         genre="Thriller",
         price=14.99,
         year_published=1980,
         description="Jack Torrance's new job at the Overlook Hotel is the perfect chance for a fresh start.",
         sold_copies=3400),

    Book(title="Gone Girl",
         author="Gillian Flynn",
         isbn=9780307588371,
         publisher="Random House Publishing Group",
         genre="Thriller",
         price=14.99,
         year_published=2014,
         description="On a warm summer morning in North Carthage, Missouri, it is Nick and Amy Dunne’s fifth wedding anniversary.",
         sold_copies=1700),

    Book(title="The Silence of Lambs",
         author="Thomas Harris",
         isbn=9780312924584,
         publisher="St. Martin's Publishing Group",
         genre="Thriller",
         price=8.99,
         year_published=1991,
         description="Hannibal Lecter. The ultimate villain of modern fiction. Read the five-million-copy bestseller that scared the world silent.",
         sold_copies=1250)
])

db.commit()

# Insert authors
db.add_all([
    Author(name="Louisa May Alcott",
           biography="Louisa May Alcott was born in Germantown, Pennsylvania on November 29, 1832. She and her three sisters, Anna, Elizabeth.",
           publisher="Barnes & Noble"),

    Author(name="Mary Shelley",
           biography="Mary Shelley was an English novelist, short story writer, dramatist, essayist, biographer, travel writer.",
           publisher="Penguin Publishing Group"),

    Author(name="Oscar Wilde",
           biography="Oscar Fingal O'Flahertie Wills Wilde was an Irish playwright, poet, and author of numerous short stories.",
           publisher="Barnes & Noble"),

    Author(name="Emily Bronte",
           biography="Emily Jane Brontë was a British novelist and poet, now best remembered for her only novel Wuthering Heights.",
           publisher="Penguin Publishing Group"),

    Author(name="Robert Louis Stevenson",
           biography="Robert Louis Balfour Stevenson was a Scottish novelist, poet, and travel writer, and a leading representative.",
           publisher="Barnes & Noble"),

    Author(name="Ray Bradbury",
           biography="Ray Douglas Bradbury, American novelist, short story writer, essayist, playwright, screenwriter and poet.",
           publisher="Simon & Schuster"),

    Author(name="Lewis Carroll",
           biography="The Reverend Charles Lutwidge Dodgson, better known by the pen name Lewis Carroll, was an English author.",
           publisher="CreateSpace Publishing"),

    Author(name="J.M. Barrie",
           biography="Sir James Matthew Barrie, 1st Baronet, OM was a Scottish author and dramatist, best remembered today as the creator. of Peter Pan.",
           publisher="Henry Holt and Co."),

    Author(name="Madeleine L'Engle",
           biography="Madeleine L'Engle was an American writer best known for her young adult fiction, particularly the Newbery Medal-winning.",
           publisher="Square Fish"),

    Author(name="L. Frank Baum",
           biography="Lyman Frank Baum was an American author, actor, and independent filmmaker best known as the creator, along with illustrator.",
           publisher="Penguin Publishing Group"),

    Author(name="Carolyn Keene",
           biography="Carolyn Keene is a writer pen name that was used by many different people- both men and women- over the years.",
           publisher="Applewood Books"),

    Author(name="Truman Capote",
           biography="Truman Capote was an American writer whose non-fiction, stories, novels and plays are recognised literary classics.",
           publisher="Knopf Doubleday Publishing Group"),

    Author(name="Erik Larson",
           biography="Erik is a former features writer for The Wall Street Journal and Time. His magazine stories have appeared in The New Yorker.",
           publisher="Crown Publishers"),

    Author(name="Vincent Bugliosi, Curt Gentry",
           biography="American attorney and author, best known for prosecuting Charles Manson and his followers for the murder of Sharon Tate.",
           publisher="W.W. Norton Company"),

    Author(name="Robert Graysmith",
           biography="ROBERT GRAYSMITH is the New York Times Bestselling author and illustrator of Zodiac , Auto Focus , and Black Fire.",
           publisher="Penguin Publishing Group"),

    Author(name="Jeff Guinn",
           biography="Jeff Guinn is a former journalist, who has won national, regional and state awards for investigative reporting.",
           publisher="Simon & Schuster"),

    Author(name="Patricia Highsmith",
           biography="Patricia Highsmith was an American novelist who is known mainly for her psychological crime thrillers.",
           publisher="W.W. Norton Company"),

    Author(name="Agatha Christie",
           biography="Agatha Christie is the best-selling author of all time. She wrote 66 crime novels and story collections.",
           publisher="HarperCollins"),

    Author(name="Stephen King",
           biography="Stephen Edwin King (born September 21, 1947) is an American author of horror, supernatural fiction, suspense.",
           publisher="New English Library"),

    Author(name="Gillian Flynn",
           biography="Gillian Flynn is an American author and television critic for Entertainment Weekly. She has so far written.",
           publisher="Random House Publishing Group"),

    Author(name="Thomas Harris",
           biography="Gillian Flynn is an American author and television critic for Entertainment Weekly. She has so far written.",
           publisher="St. Martin's Publishing Group")
])

db.commit()

# Insert users
db.add_all([
    User(name="Fernando",
         username = "Fernando",
         email= "Fernando@fiu.edu",
         home_address = "123 SW 56 street",
         password= 123),

    User(name="Sasha",
        username = "Sasha",
        email= "Sasha@fiu.edu",
        home_address = "354 NW 44 street",
        password= 123),

    User(name="Thamare",
         username = "Thamare",
         email= "Thamare@fiu.edu",
         home_address = "789 SW 22 street",
         password= 123),

    User(name="Karim",
         username = "Karim",
         email= "Karim@fiu.edu",
         home_address = "555 NW 10 street",
         password= 123),

    User(name="Sebastian",
         username = "Sebastian",
         email= "Sebastian@fiu.edu",
         home_address = "965 SW 30 street",
         password= 123),

    User(name="Camilo",
         username = "Camilo",
         email= "Camilo@fiu.edu",
         home_address = "523 NW 16 street",
         password= 123),                    
])

db.commit()

db.close()
