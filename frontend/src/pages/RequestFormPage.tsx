import { useMutation, useQueryClient } from "@tanstack/react-query";
import { useState } from "react";
import { createRequest } from "../api/client";
import RequestForm from "../components/RequestForm";
import type { ServiceRequestCreate } from "../types";

export default function RequestFormPage() {
  const queryClient = useQueryClient();
  const [apiError, setApiError] = useState<string | null>(null);

  const mutation = useMutation({
    mutationFn: (payload: ServiceRequestCreate) => createRequest(payload),
    onSuccess: async () => {
      setApiError(null);
      await queryClient.invalidateQueries({ queryKey: ["requests"] });
      await queryClient.invalidateQueries({ queryKey: ["reliability"] });
    },
    onError: (error: Error) => {
      setApiError(error.message);
    },
  });

  return (
    <RequestForm
      submitting={mutation.isPending}
      apiError={apiError}
      onSubmit={async (payload) => {
        setApiError(null);
        await mutation.mutateAsync(payload);
      }}
    />
  );
}
