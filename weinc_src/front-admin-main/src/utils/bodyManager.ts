export const toggleBodyClass = (addRemoveClass: string, className: string) => {
  const el = document.body;

  if (addRemoveClass === 'addClass') {
    el.classList.add(className);
  } else {
    el.classList.remove(className);
  }
};
