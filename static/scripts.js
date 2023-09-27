document.addEventListener("DOMContentLoaded", function () {
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

// Render topics to the DOM
function renderTopics(topics) {
  const container = document.getElementById("topicsContainer");
  container.innerHTML = "";  // Clear existing topics

  topics.forEach((topic, index) => {
    const topicDiv = document.createElement("div");
    topicDiv.textContent = topic;

    // Add delete button
    const deleteButton = document.createElement("button");
    deleteButton.textContent = "Delete";
    deleteButton.addEventListener("click", () => deleteTopic(index));
    topicDiv.appendChild(deleteButton);

    container.appendChild(topicDiv);
  });
}

// Add a new topic
function addTopic(newTopic) {
  const topics = JSON.parse(localStorage.getItem('topics'));
  topics.push(newTopic);
  localStorage.setItem('topics', JSON.stringify(topics));
  renderTopics(topics);
}

// Delete a topic by index
function deleteTopic(index) {
  const topics = JSON.parse(localStorage.getItem('topics'));
  topics.splice(index, 1);  // Remove the topic at the given index
  localStorage.setItem('topics', JSON.stringify(topics));
  renderTopics(topics);
}
