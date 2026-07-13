import { Component } from "react";

// React Error Boundaries must be class components — there is no hook
// equivalent yet. It catches render-time errors anywhere in its subtree,
// logs them, and shows a fallback UI instead of a blank crashed page.
class ErrorBoundary extends Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error("Unhandled UI error:", error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="error-boundary-fallback">
          <h2>Something went wrong</h2>
          <p>
            The page hit an unexpected error. Try reloading, and if the
            problem continues, please let the site owner know.
          </p>
          <button onClick={() => window.location.reload()}>Reload</button>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
