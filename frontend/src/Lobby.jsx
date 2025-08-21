import { useState } from "react";
import { Steps } from "./Steps";
import { Modal } from "./Modal";

export const Lobby = () => {
	const [modalFade, setModalFade] = useState(false);
	return (
		<>
			{!modalFade ? (
				<div className="text-white flex justify-center items-center flex-col">
					<h1>GIFTLY</h1>
					<p> Portar diseñado para generar de manera aleatoria y personalizada sorteos para intercambios secretos</p>
					<button
						onClick={() => setModalFade(!modalFade)}
						className="text-black mt-10 font-bold w-34 h-10 text-xs rounded-xl bg-amber-100 cursor-pointer hover:scale-105 transition transform hover:bg-amber-200">
						CREAR UN EVENTO
					</button>
				</div>
			) : (
				<div className="bg-white size-1/2 p-10 rounded-md flex justify-between">
					<Steps modalFade={modalFade} setModalFade={setModalFade} />
					<Modal />
				</div>
			)}
		</>
	);
};
