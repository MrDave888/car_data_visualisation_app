from database import init_db, is_seeded
import seeders.seed as seeder


def main():
    init_db()

    if not is_seeded():
        print('Database is empty — seeding from Kaggle...')
        seeder.run()
        print('Seeding complete.')
    else:
        print('Database already seeded, skipping download.')

    # Your visualisation / analysis code goes here


if __name__ == '__main__':
    main()
