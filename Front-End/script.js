function deleteDiv() {
    // Find the closest `.card` div containing the button
    const button = event.target; // The button that was clicked
    const cardDiv = button.closest('.card'); // Closest parent div with the class 'card'

    if (cardDiv) {
        cardDiv.remove(); // Remove the div from the DOM
        console.log("Card div removed successfully.");
    } else {
        console.log("No card div found.");
    }
}


