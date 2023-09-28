document.addEventListener("DOMContentLoaded", function () {
  // Check if service workers are supported by the browser
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/service-worker.js')
      .then(function (registration) {
        console.log('Service Worker registered with scope:', registration.scope);
      })
      .catch(function (error) {
        console.log('Service Worker registration failed:', error);
      });
  }
  // Initialize with default topics if Local Storage is empty
  if (!localStorage.getItem('topics')) {
    localStorage.setItem('topics', JSON.stringify(["World", "Canada"]));
  }

  // Load topics from Local Storage and render them
  const topics = JSON.parse(localStorage.getItem('topics'));
  renderTopics(topics);

  // Listen for form submissions to add new topics
  document.getElementById("addTopicForm").addEventListener("submit", function (e) {
    e.preventDefault();
    const newTopic = document.getElementById("newTopic").value;
    if (newTopic) {
      addTopic(newTopic);
    }
  });
});

function renderTopics(topics) {
  const container = document.getElementById("topicsContainer");
  container.innerHTML = "";

  topics.forEach((topic, index) => {
    const topicDiv = document.createElement("div");
    topicDiv.className = "topic-item"; 

    // Create div for text
    const textDiv = document.createElement("div");
    textDiv.className = "text";
    textDiv.textContent = topic;
    topicDiv.appendChild(textDiv);

    const deleteButton = document.createElement("button");
    deleteButton.className = "delete-button"; 
    deleteButton.textContent = "Delete";
    deleteButton.addEventListener("click", () => deleteTopic(index));

    // Create div for button
    const buttonDiv = document.createElement("div");
    buttonDiv.className = "button";
    buttonDiv.appendChild(deleteButton);
    topicDiv.appendChild(buttonDiv);

    container.appendChild(topicDiv);
  });
}

// Add a new topic
function addTopic(newTopic) {
  const topics = JSON.parse(localStorage.getItem('topics'));
  topics.push(newTopic);
  localStorage.setItem('topics', JSON.stringify(topics));
  renderTopics(topics);
  location.reload();
}

// Delete a topic by index
function deleteTopic(index) {
  const topics = JSON.parse(localStorage.getItem('topics'));
  topics.splice(index, 1);  // Remove the topic at the given index
  localStorage.setItem('topics', JSON.stringify(topics));
  renderTopics(topics);
}
