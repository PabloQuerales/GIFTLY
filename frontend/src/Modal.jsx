import { useState } from "react";

export const Modal = (props) => {
	const [inputValue, setInputValue] = useState("");
	const handleChange = (e) => {
		setInputValue(e.target.value);
	};
	const handleClick = () => {
		console.log(inputValue);
		setInputValue("");
	};
	return (
		<div
			onSubmit={handleClick}
			className="fixed inset-0 z-50 grid place-content-center bg-black/50 p-4"
			role="dialog"
			aria-modal="true"
			aria-labelledby="modalTitle">
			<div className="w-full max-w-md rounded-lg bg-white p-6 shadow-lg animate-rubber-band">
				<div className="flex items-start justify-between">
					<h2 id="modalTitle" className="text-xl font-bold text-amber-900 sm:text-2xl">
						Bienvenido a GIFTLY
					</h2>

					<button
						type="button"
						className="-me-4 -mt-4 rounded-full p-2 text-gray-400 transition-colors hover:bg-gray-50 hover:text-gray-600 focus:outline-none"
						aria-label="Close"
						onClick={() => props.setModalFade(!props.modalFade)}>
						<svg xmlns="http://www.w3.org/2000/svg" className="size-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
							<path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
						</svg>
					</button>
				</div>

				<div className="mt-4">
					<p className="text-gray-700">Para empezar, te haremos algunas preguntas sencillas que nos ayudarán a crear tu evento de intercambios.</p>

					<label htmlFor="Confirm" className="mt-4 block">
						<span className="text-sm text-gray-700 font-bold">¡Comencemos por tu nombre!</span>

						<input
							type="text"
							id="Confirm"
							value={inputValue}
							onChange={handleChange}
							className="mt-0.5 p-2 w-full rounded border-gray-300 shadow-sm sm:text-sm"
						/>
					</label>
				</div>

				<footer className="mt-6 flex justify-end gap-2">
					<button
						type="button"
						className="rounded bg-gray-100 px-4 py-2 text-sm font-medium text-gray-700 transition-colors hover:bg-gray-200"
						onClick={() => props.setModalFade(!props.modalFade)}>
						Cancelar
					</button>

					<button
						type="button"
						onClick={handleClick}
						className="rounded bg-blue-600 px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-blue-700">
						Continuar
					</button>
				</footer>
			</div>
		</div>
	);
};
