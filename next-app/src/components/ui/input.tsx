import * as React from "react";

export const Input = React.forwardRef<HTMLInputElement, React.InputHTMLAttributes<HTMLInputElement>>(
  ({ className = "", ...props }, ref) => (
    <input ref={ref} className={`px-3 py-2 rounded bg-neutral-900 border border-neutral-700 text-white ${className}`} {...props} />
  )
);
Input.displayName = "Input";
