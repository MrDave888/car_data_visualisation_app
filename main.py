import sys
from PySide6.QtWidgets import QApplication
from database import init_db, is_seeded
import seeders.seed as seeder
from ui.main_window import MainWindow


def main():
    init_db()

    if not is_seeded():
        print('Database is empty — seeding from Kaggle...')
        seeder.run()
        print('Seeding complete.')
    else:
        print('Database already seeded, skipping download.')

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
