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
		<div className="w-auto ms-10 flex flex-col items-center text-center border-l-2 pl-4">
			<div className="flex items-start justify-between">
				<h2 id="modalTitle" className="text-xl font-bold text-amber-900 sm:text-2xl">
					Bienvenido a GIFTLY
				</h2>
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
	);
};
