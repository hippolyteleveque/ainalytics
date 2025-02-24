import React from "react";

const Spinner = () => {
  return (
    <div className="flex inline-flex items-center justify-center w-full h-full">
      <div
        className="h-10 w-10 animate-spin rounded-full border-2 border-gray-300 border-t-gray-900"
        aria-label="Loading..."
      />
    </div>
  );
};

export default Spinner;
