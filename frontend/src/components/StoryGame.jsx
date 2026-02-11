import { useState, useMemo } from "react";

function StoryGame({ story, onNewStory }) {
  // Initialize from props directly
  const [currentNodeId, setCurrentNodeId] = useState(
    story?.root_node?.id || null,
  );

  // Calculate derived state using useMemo
  const { currentNode, options, isEnding, isWinningEnding } = useMemo(() => {
    if (currentNodeId && story?.all_nodes) {
      const node = story.all_nodes[currentNodeId];

      return {
        currentNode: node,
        options:
          !node.is_ending && node.options && node.options.length > 0
            ? node.options
            : [],
        isEnding: node.is_ending,
        isWinningEnding: node.is_winning_endig,
      };
    }

    return {
      currentNode: null,
      options: [],
      isEnding: false,
      isWinningEnding: false,
    };
  }, [currentNodeId, story]);

  const chooseOption = (optionId) => {
    setCurrentNodeId(optionId);
  };

  const restartStory = () => {
    if (story && story.root_node) {
      setCurrentNodeId(story.root_node.id);
    }
  };

  return (
    <div className="story-game">
      <header className="story-header">
        <h2>{story.title}</h2>
      </header>

      <div className="story-content">
        {currentNode && (
          <div className="story-node">
            <p>{currentNode.content}</p>

            {isEnding ? (
              <div className="story-ending">
                <h3>{isWinningEnding ? "Congratulations" : "The End"}</h3>
                {isWinningEnding
                  ? "You reached a winning ending"
                  : "Your adventure has ended."}
              </div>
            ) : (
              <div className="story-options">
                <h3>What will you do?</h3>
                <div className="options-list">
                  {options.map((option, index) => {
                    return (
                      <button
                        key={index}
                        onClick={() => chooseOption(option.node_id)}
                        className="option-btn"
                      >
                        {option.text}
                      </button>
                    );
                  })}
                </div>
              </div>
            )}
          </div>
        )}

        <div className="story-controls">
          <button onClick={restartStory} className="reset-btn">
            Restart Story
          </button>
        </div>

        {onNewStory && (
          <button onClick={onNewStory} className="new-story-btn">
            New Story
          </button>
        )}
      </div>
    </div>
  );
}

export default StoryGame;
