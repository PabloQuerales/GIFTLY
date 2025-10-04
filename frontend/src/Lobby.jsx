import { useState } from "react";
import { Steps } from "./Steps";
import { Modal } from "./Modal";
import logo from "../src/assets/logo.png";

export const Lobby = () => {
	const [modalFade, setModalFade] = useState(false);
	return (
		<>
			{!modalFade ? (
				<div className="text-white flex justify-center items-center flex-col">
					<img src={logo} className="w-80 absolute top-10 logo-giftly-sombra" />
					<p className="text-lg"> Portar diseñado para generar de manera aleatoria y personalizada sorteos para intercambios secretos</p>
					<button
						onClick={() => setModalFade(!modalFade)}
						className="text-black mt-10 font-bold w-34 h-10 text-xs rounded-xl bg-[#FF6B6B] cursor-pointer hover:scale-105 transition transform hover:bg-red-300">
						CREAR UN EVENTO
					</button>
				</div>
			) : (
				<div className="flex justify-center  items-center size-full overflow-hidden">
					<a href="">
						<img src="./src/assets/g-logo.png" alt="logo-giftly" className="absolute top-5 left-5 size-20 animate-fade-in-down" />
					</a>
					<img src="./src/assets/decor.png" alt="logo-giftly" className="absolute animate-fade-in-down -right-15 -bottom-12 size-100 " />
					<div className="h-2/3 w-1/2  p-10 rounded-md flex justify-between animate-fade-in-down bg-gradient-to-tr to-gray-200 from-gray-300">
						<Steps />
						<Modal modalFade={modalFade} setModalFade={setModalFade} />
					</div>
				</div>
			)}
		</>
	);
};
