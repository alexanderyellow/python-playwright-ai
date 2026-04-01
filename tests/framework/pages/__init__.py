from .alerts_frames_windows.alerts_page import AlertsPage
from .alerts_frames_windows.modal_dialogs_page import ModalDialogsPage
from .base_page import BasePage
from .book_store.book_store_page import BookStorePage
from .book_store.login_page import BookStoreLoginPage
from .elements.check_box_page import CheckBoxPage
from .elements.text_box_page import TextBoxPage
from .forms.practice_form_page import PracticeFormPage
from .interactions.droppable_page import DroppablePage
from .interactions.selectable_page import SelectablePage
from .widgets.date_picker_page import DatePickerPage
from .widgets.slider_page import SliderPage

__all__ = [
    "AlertsPage",
    "BasePage",
    "BookStoreLoginPage",
    "BookStorePage",
    "CheckBoxPage",
    "DatePickerPage",
    "DroppablePage",
    "ModalDialogsPage",
    "PracticeFormPage",
    "SelectablePage",
    "SliderPage",
    "TextBoxPage",
]
