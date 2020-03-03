let store = {
  notifications: []
};

function addNotification(text, error = false) {
  let id = Math.random().toString(36).substr(2, 9);
  let style = {bottom: 0, };
  store.notifications.forEach(() => {
    style.bottom += 70;
  });
  style.bottom = style.bottom + 'px';
  let notif = {id: id, text: text, style: style, error: error};
  store.notifications.splice(0, 0, notif);
  setTimeout(() => removeNotification(notif), 5000);
}

function removeNotification(original_notif) {
  store.notifications = store.notifications.filter((notif) => {
    return notif.id !== original_notif.id;
  });
}


export default {
  addNotification,
  removeNotification,
  store
}
