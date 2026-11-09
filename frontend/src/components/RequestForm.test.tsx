import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";
import RequestForm from "./RequestForm";

describe("RequestForm", () => {
  it("shows validation errors for empty submit", async () => {
    const user = userEvent.setup();
    const onSubmit = vi.fn();
    render(<RequestForm onSubmit={onSubmit} />);
    await user.click(screen.getByRole("button", { name: /submit request/i }));
    expect(screen.getByText(/customer name is required/i)).toBeInTheDocument();
    expect(onSubmit).not.toHaveBeenCalled();
  });

  it("submits a valid payload", async () => {
    const user = userEvent.setup();
    const onSubmit = vi.fn().mockResolvedValue(undefined);
    render(<RequestForm onSubmit={onSubmit} />);

    await user.type(screen.getByLabelText(/customer name/i), "Alex Customer");
    await user.type(screen.getByLabelText(/customer email/i), "alex@example.com");
    await user.type(screen.getByLabelText(/request title/i), "Broken pump");
    await user.type(screen.getByLabelText(/description/i), "Pump will not start after power cycle.");
    await user.click(screen.getByRole("button", { name: /submit request/i }));

    expect(onSubmit).toHaveBeenCalledWith(
      expect.objectContaining({
        customer_name: "Alex Customer",
        customer_email: "alex@example.com",
        title: "Broken pump",
      }),
    );
  });

  it("renders API failure message", () => {
    render(<RequestForm onSubmit={vi.fn()} apiError="Service temporarily unavailable" />);
    expect(screen.getByText(/service temporarily unavailable/i)).toBeInTheDocument();
  });
});
