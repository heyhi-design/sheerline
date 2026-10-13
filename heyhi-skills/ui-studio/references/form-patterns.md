---
name: form-patterns
zone: 2
load_trigger: Build requires forms — validation, dynamic fields, multi-step flows, or headless component integration with React Hook Form
token_estimate: ~750
classification: HeyHi Internal Use Only
created: 2026-04-18
version: "1.0.0"
dependencies:
  - heyhi-skills/ui-studio/references/component-architecture.md
---

# Form Patterns

Reference for React form work using React Hook Form + Zod. Load when a build includes any non-trivial form — validation, headless component integration, dynamic fields, or multi-step flows.

**Soft dependency:** `component-architecture.md` covers Radix Select and other headless components used in the `Controller` examples below. Load it first if you need the full headless component context.

---

## The Stack

**React Hook Form** handles form performance via uncontrolled inputs — minimal re-renders, no controlled state per field. **Zod** handles validation schemas with TypeScript type inference. Together they give a single source of truth for shape, validation, and types.

---

## Basic Pattern

```typescript
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

// Schema is the single source of truth for shape and validation
const schema = z.object({
  name: z.string().min(2, 'Name must be at least 2 characters'),
  email: z.string().email('Invalid email address'),
  budget: z.number().min(0).optional(),
});

type FormValues = z.infer<typeof schema>; // TypeScript type inferred from schema

function ContactForm() {
  const {
    register,
    handleSubmit,
    formState: { errors }
  } = useForm<FormValues>({
    resolver: zodResolver(schema)
  });

  const onSubmit = async (data: FormValues) => {
    // data is fully typed and validated before reaching this handler
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <div>
        <label htmlFor="name">Name</label>
        <input
          id="name"
          {...register('name')}
          aria-invalid={!!errors.name}
          aria-describedby="name-error"
        />
        {errors.name && (
          <p id="name-error" role="alert">{errors.name.message}</p>
        )}
      </div>
      {/* ... */}
    </form>
  );
}
```

**Accessibility pattern for errors:**
- `aria-invalid={!!errors.field}` marks the field as invalid when there's an error.
- `aria-describedby="field-error"` links the input to its error message.
- `role="alert"` on the error `<p>` announces the error to screen readers when it appears.

---

## Controller — Headless and Custom Components

`register` works for native HTML inputs. For any component that isn't a native input — Radix Select, custom pickers, headless dropdowns — use `Controller`.

```typescript
import { useForm, Controller } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as Select from '@radix-ui/react-select';
import { z } from 'zod';

const schema = z.object({
  category: z.string().min(1, 'Select a category'),
});

type FormValues = z.infer<typeof schema>;

const categories = [
  { value: 'retirement', label: 'Retirement' },
  { value: 'brokerage', label: 'Brokerage' },
  { value: 'savings', label: 'Savings' },
];

function CategoryForm() {
  const { control, handleSubmit, formState: { errors } } = useForm<FormValues>({
    resolver: zodResolver(schema),
  });

  return (
    <form onSubmit={handleSubmit(console.log)}>
      <Controller
        name="category"
        control={control}
        render={({ field }) => (
          <Select.Root value={field.value} onValueChange={field.onChange}>
            <Select.Trigger
              aria-invalid={!!errors.category}
              aria-describedby={errors.category ? 'category-error' : undefined}
            >
              <Select.Value placeholder="Select a category" />
            </Select.Trigger>
            <Select.Portal>
              <Select.Content>
                <Select.Viewport>
                  {categories.map(opt => (
                    <Select.Item key={opt.value} value={opt.value}>
                      <Select.ItemText>{opt.label}</Select.ItemText>
                    </Select.Item>
                  ))}
                </Select.Viewport>
              </Select.Content>
            </Select.Portal>
          </Select.Root>
        )}
      />
      {errors.category && (
        <p id="category-error" role="alert">{errors.category.message}</p>
      )}
    </form>
  );
}
```

**The pattern:** `field.value` feeds the current form value into the component. `field.onChange` notifies RHF of changes. `aria-invalid` and `aria-describedby` on the `Trigger` preserve accessible error state through the headless abstraction.

---

## Dynamic Fields: useFieldArray

Required for any form where users add or remove items — account entries, beneficiary lists, asset additions, document uploads.

```typescript
import { useForm, useFieldArray } from 'react-hook-form';

const schema = z.object({
  accounts: z.array(z.object({
    institution: z.string().min(1, 'Institution required'),
    balance: z.number().min(0, 'Balance must be non-negative'),
  })).min(1, 'Add at least one account'),
});

type FormValues = z.infer<typeof schema>;

function AccountsForm() {
  const { register, control, handleSubmit, formState: { errors } } = useForm<FormValues>({
    resolver: zodResolver(schema),
    defaultValues: { accounts: [{ institution: '', balance: 0 }] }
  });

  const { fields, append, remove } = useFieldArray({ control, name: 'accounts' });

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      {fields.map((field, index) => (
        <fieldset key={field.id}> {/* Use field.id — NOT index — as the key */}
          <legend>Account {index + 1}</legend>
          <input
            {...register(`accounts.${index}.institution`)}
            aria-label={`Institution for account ${index + 1}`}
          />
          {errors.accounts?.[index]?.institution && (
            <p role="alert">{errors.accounts[index].institution.message}</p>
          )}
          <input
            type="number"
            {...register(`accounts.${index}.balance`, { valueAsNumber: true })}
            aria-label={`Balance for account ${index + 1}`}
          />
          <button type="button" onClick={() => remove(index)}>
            Remove account {index + 1}
          </button>
        </fieldset>
      ))}
      <button type="button" onClick={() => append({ institution: '', balance: 0 })}>
        Add account
      </button>
      <button type="submit">Save</button>
    </form>
  );
}
```

**Two critical details:**
1. Use `field.id` (not `index`) as the React key — RHF generates stable IDs that survive reordering. Using index causes React to misidentify elements when items are removed from the middle.
2. Use `valueAsNumber: true` for numeric inputs — prevents string coercion on submission. Without this, a number input registers as a string and Zod will reject it.

---

## Multi-Step Forms

Keep a single form instance across all steps. Do not create a new `useForm` per step.

```typescript
// Single form instance — persist across steps
const form = useForm<FormValues>({
  resolver: zodResolver(schema),
  defaultValues: { ... }
});

// Step machine — separate from the form
const [step, setStep] = useState(0);

// Validate only the fields in the current step before advancing
const handleNext = async () => {
  const stepFields = getFieldsForStep(step); // ['name', 'email']
  const valid = await form.trigger(stepFields);
  if (valid) setStep(s => s + 1);
};
```

---

## Server Validation

Zod schemas can run server-side as well as client-side — use the same schema in both contexts.

```typescript
// In Next.js Server Actions
import { schema } from './validation';

async function submitForm(formData: FormData) {
  'use server';
  const result = schema.safeParse(Object.fromEntries(formData));
  if (!result.success) {
    return { errors: result.error.flatten() };
  }
  // ... process validated data
}
```

This gives single-source-of-truth validation across the client/server boundary.

---

## Common Mistakes

| Mistake | Correct behavior |
|---------|-----------------|
| `key={index}` in `useFieldArray` | `key={field.id}` — stable across reorders/removals |
| Missing `valueAsNumber: true` on number inputs | Zod `z.number()` fails on string values |
| Using `register` on a Radix or custom component | Wrap in `Controller` instead |
| Creating a new `useForm` per step in multi-step forms | Single form instance, step machine is separate |
| Forgetting `role="alert"` on error elements | Error messages won't be announced on appearance |

---

*HeyHi Internal Use Only. Zone 2 — task-conditional. Load when build includes non-trivial forms with validation, dynamic fields, or headless component integration. v1.0.0 created 2026-04-18 from frontend-research-reference.md v1.2.0.*
